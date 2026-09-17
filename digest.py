"""
digest.py — Session 8: SHIP a useful agent that runs without your laptop.

Sessions 6-7 built an agent and made it reliable. This session makes it USEFUL
and puts it in the cloud on a schedule. It's your morning brief:

  1. FETCHES several news feeds (AI + markets, tuned to your holdings),
  2. asks the model to write a structured brief (top story + why-it-matters),
  3. DELIVERS it two ways — writes digest.html (published on your website) and
     emails it to you.

The agent LOOP and GUARDRAILS are the ones from agent2.py: a step limit,
defensive tools that return "ERROR:" instead of crashing, and output trimming.

What's NEW this session is all about SHIPPING:
  - SECRETS FROM THE ENVIRONMENT (not a file), so the SAME code runs on your Mac
    and in the cloud where there's no key.txt;
  - TWO DELIVERY CHANNELS (a web page + an email);
  - and a SCHEDULE in the cloud (see .github/workflows/digest.yml).

The brief is written by SONNET (richer synthesis than Haiku) with an automatic
fall back to Haiku if Sonnet is ever unavailable — model choice is a cost lever,
and a fallback is a reliability guardrail.

Run locally:  cd ~/Documents/"Claude project"  then  python3 digest.py
(Email is skipped automatically until the email secrets are set.)
"""

import os
import re
import ssl
import html
import smtplib
import datetime
import urllib.request
from email.message import EmailMessage
from anthropic import Anthropic


# =============================================================================
# PART 0 — SECRETS: environment variables, with a local .env for convenience.
# =============================================================================

here = os.path.dirname(os.path.abspath(__file__))


def _load_local_env(filename="secrets.env"):
    """DEV CONVENIENCE: load KEY=VALUE lines from a gitignored local file into
    the environment, so you never paste secrets into your shell. In the cloud
    there IS no secrets.env — the same values arrive as real environment
    variables from GitHub Secrets. Real env vars always win."""
    path = os.path.join(here, filename)
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_local_env()


def get_secret(env_name, file_fallback=None):
    """Return a secret from the environment, or from a local file, or None."""
    val = os.environ.get(env_name)
    if val:
        return val.strip()
    if file_fallback:
        path = os.path.join(here, file_fallback)
        if os.path.exists(path):
            with open(path) as f:
                return f.read().strip()
    return None


api_key = get_secret("ANTHROPIC_API_KEY", file_fallback="key.txt")
if not api_key:
    raise SystemExit("No API key: set ANTHROPIC_API_KEY, or keep key.txt (Session 5).")

client = Anthropic(api_key=api_key)

GMAIL_ADDRESS = get_secret("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = get_secret("GMAIL_APP_PASSWORD")
DIGEST_TO = get_secret("DIGEST_TO") or GMAIL_ADDRESS


# =============================================================================
# PART 1 — The one tool: fetch_url (defensive + trimmed — from agent2).
#
# Trim is bigger now (9000 chars) so the model sees MORE headlines per feed —
# that's the main dial for "the brief felt thin." More chars = more input tokens
# = a little more cost, which is exactly the trade-off you're now making on
# purpose.
# =============================================================================

FETCH_CHARS = 9000

def fetch_url(url):
    """Download a page/feed and return its text — or an ERROR string if it fails."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "tim-digest-agent"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        return text[:FETCH_CHARS]
    except Exception as e:
        return f"ERROR: could not fetch {url} ({type(e).__name__}: {e})"


TOOL_FUNCTIONS = {"fetch_url": fetch_url}

TOOLS = [{
    "name": "fetch_url",
    "description": "Download a web page or RSS feed and return its text. On failure "
                   "it returns a string starting with 'ERROR:' — treat that source "
                   "as unavailable and carry on with the others.",
    "input_schema": {
        "type": "object",
        "properties": {"url": {"type": "string", "description": "Full URL to fetch."}},
        "required": ["url"],
    },
}]


# =============================================================================
# PART 2 — What to read, and the brief to write.
#
# Seven feeds across four providers (Google News, The Verge, Hacker News, CNBC),
# so no single provider is load-bearing. Markets feeds are aimed at YOUR book:
# big tech, semiconductors, and storage/memory.
# =============================================================================

SOURCES = [
    # ---------- AI & TECH ----------
    # 1) Google News — broad AI coverage aggregated across many outlets.
    "https://news.google.com/rss/search?q=artificial+intelligence+when:1d&hl=en-US&gl=US&ceid=US:en",
    # 2) Google News — AI business: funding, deals, M&A, big-lab moves.
    "https://news.google.com/rss/search?q=(AI+funding+OR+AI+startup+OR+AI+acquisition+OR+OpenAI+OR+Anthropic)+when:1d&hl=en-US&gl=US&ceid=US:en",
    # 3) The Verge — a direct publisher feed (a provider that isn't Google).
    "https://www.theverge.com/rss/index.xml",
    # 4) Hacker News front page — the builder/industry pulse.
    "https://hnrss.org/frontpage?points=100",

    # ---------- MARKETS, aimed at YOUR exposure ----------
    # 5) Google News — your names and their AI-capex theme.
    "https://news.google.com/rss/search?q=(Nvidia+OR+Microsoft+OR+semiconductor+OR+%22Western+Digital%22+OR+Seagate+OR+%22data+center%22)+stock+when:1d&hl=en-US&gl=US&ceid=US:en",
    # 6) Google News — semiconductors & storage/memory specifically.
    "https://news.google.com/rss/search?q=(semiconductor+OR+NAND+OR+HBM+OR+memory+chip+OR+Micron+OR+%22SK+Hynix%22+OR+Seagate)+when:1d&hl=en-US&gl=US&ceid=US:en",
    # 7) CNBC Markets — a direct business-press feed.
    "https://www.cnbc.com/id/20910258/device/rss/rss.html",
]

TODAY = datetime.date.today().strftime("%A, %d %B %Y")

_numbered = "\n".join(f"  {i + 1}. {u}" for i, u in enumerate(SOURCES))

TASK = f"""You are my morning news analyst, writing for an AI commercial leader
(hyperscaler partnerships, APAC, invested in big tech + semiconductors + storage).
Today is {TODAY}.

Fetch EACH of these {len(SOURCES)} RSS feeds with the fetch_url tool:
{_numbered}

Every RSS <item> has a <title>, a short <description>, and a <link> URL. Use the
<link> so you can cite each story as a clickable Markdown link.

Then write a rich but scannable morning brief in Markdown with EXACTLY this shape:

# Morning Brief — {TODAY}

## Top Story
The single most important development for someone in AI/tech commercial strategy,
in 2-3 sentences: what happened, and why it's today's lead. Link the story.

## AI — Research & Models
- 2 to 3 bullets on new models, capabilities, or research.

## AI — Business & Funding
- 2 to 3 bullets on funding, deals, M&A, product launches, big-lab moves.

## AI — Policy & Regulation
- 1 to 2 bullets on governance, regulation, geopolitics. If nothing notable,
  write a single bullet saying "Quiet on the policy front today."

## Markets — Your Holdings
- 2 to 3 bullets on big tech, semiconductors, and storage/memory names
  (Nvidia, Microsoft, Western Digital, Seagate, Micron, SK Hynix, etc.).

## Markets — Macro
- 1 to 2 bullets on indices, the Fed, rates, and the broad risk mood.

## Sources checked
- One line: how many feeds you read, and name any you could NOT read.

FORMAT RULES for every bullet:
- Start with the story as a Markdown link: [headline](the item's link URL).
- Then " — why it matters:" and one clause on the commercial/strategic angle.
Base everything ONLY on the fetched headlines — never invent news. If a feed
returns an ERROR, skip it and note it in "Sources checked". Aim for 400-550 words.
Output ONLY the Markdown, with nothing before or after it."""


# =============================================================================
# PART 3 — The agent loop + guardrails, now with a MODEL FALLBACK.
#
# We write with Sonnet (richer). If Sonnet is ever unavailable, we fall back to
# Haiku and keep going — a model outage should never mean no brief. That's the
# same "degrade gracefully" instinct as the defensive tools, applied to the model
# itself. Model choice + fallback are your cost and reliability levers.
# =============================================================================

PRIMARY_MODEL = "claude-sonnet-4-5-20250929"   # richer synthesis for a brief you read
FALLBACK_MODEL = "claude-haiku-4-5-20251001"   # cheap, dependable safety net
MAX_STEPS = 14                                 # circuit breaker: enough for 7 feeds


def run_agent(task):
    """Run the loop. Returns (final_markdown, steps_used, hit_limit, model_used)."""
    messages = [{"role": "user", "content": task}]
    model = PRIMARY_MODEL
    step = 0
    final_text = ""
    print(f"(writing with {model})")
    while step < MAX_STEPS:
        step += 1
        try:
            response = client.messages.create(
                model=model, max_tokens=3000, tools=TOOLS, messages=messages,
            )
        except Exception as e:
            msg = str(e).lower()
            if model != FALLBACK_MODEL and ("not_found" in msg or "404" in msg or "model" in msg):
                print(f"[model] {model} unavailable ({type(e).__name__}) — "
                      f"falling back to {FALLBACK_MODEL}")
                model = FALLBACK_MODEL
                step -= 1
                continue
            raise

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"[step {step}] fetch: {block.input.get('url', '')[:65]}...")
                    output = TOOL_FUNCTIONS[block.name](**block.input)
                    flag = "  <-- ERROR" if output.startswith("ERROR:") else ""
                    print(f"[step {step}] got {len(output)} chars{flag}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": output,
                    })
            messages.append({"role": "user", "content": tool_results})
            continue

        for block in response.content:
            if block.type == "text":
                final_text += block.text
        print(f"\n(Brief written in {step} model calls, using {model}.)")
        return final_text.strip(), step, False, model

    print(f"\n!! STEP LIMIT ({MAX_STEPS}) reached — stopped before finishing.")
    return final_text.strip(), step, True, model


# =============================================================================
# PART 4 — DELIVERY #1: publish a web page.
#
# The model hands back Markdown. We do a tiny Markdown -> HTML conversion that
# now understands headings, bullets, **bold**, AND [links](urls), then wrap it in
# a styled page saved as digest.html. GitHub Actions commits that file, and Pages
# publishes it to https://iamtimbrown.github.io/digest.html
# =============================================================================

_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _inline(text):
    """Escape HTML, then render [label](url) links and **bold** safely."""
    out, last = "", 0
    for m in _LINK.finditer(text):
        out += html.escape(text[last:m.start()])
        label = html.escape(m.group(1))
        url = html.escape(m.group(2), quote=True)
        out += f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'
        last = m.end()
    out += html.escape(text[last:])
    while "**" in out:
        out = out.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
    return out


def md_to_html(md):
    """A minimal Markdown -> HTML converter: headings, bullets, links, bold."""
    out, in_list = [], False
    for raw in md.splitlines():
        line = raw.rstrip()
        if line.startswith("## "):
            if in_list:
                out.append("</ul>"); in_list = False
            out.append(f"<h2>{_inline(line[3:].strip())}</h2>")
        elif line.startswith("# "):
            if in_list:
                out.append("</ul>"); in_list = False
            out.append(f"<h1>{_inline(line[2:].strip())}</h1>")
        elif line.startswith("- ") or line.startswith("* "):
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{_inline(line[2:].strip())}</li>")
        elif line == "":
            if in_list:
                out.append("</ul>"); in_list = False
        else:
            if in_list:
                out.append("</ul>"); in_list = False
            out.append(f"<p>{_inline(line)}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Morning Brief</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
         max-width: 680px; margin: 40px auto; padding: 0 20px; line-height: 1.55;
         color: #1a1a1a; background: #fafafa; }}
  h1 {{ font-size: 1.6rem; margin-bottom: 0.2rem; }}
  h2 {{ font-size: 1.1rem; margin-top: 1.6rem; color: #111;
        border-bottom: 1px solid #e5e5e5; padding-bottom: 4px; }}
  li {{ margin: 0.5rem 0; }}
  a {{ color: #2563eb; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .stamp {{ color: #888; font-size: 0.85rem; margin-bottom: 1.5rem; }}
  .foot {{ color: #aaa; font-size: 0.8rem; margin-top: 2.5rem;
           border-top: 1px solid #eee; padding-top: 10px; }}
</style>
</head>
<body>
{body}
<p class="stamp">Generated {stamp} · <a href="index.html">home</a></p>
<p class="foot">Built by digest.py — an agent that fetches, summarises, and ships itself. Session 8.</p>
</body>
</html>
"""


def write_web_page(md):
    """Render the Markdown brief into digest.html next to this script."""
    stamp = datetime.datetime.now().strftime("%A, %d %B %Y at %H:%M")
    page = PAGE_TEMPLATE.format(body=md_to_html(md), stamp=stamp)
    out_path = os.path.join(here, "digest.html")
    with open(out_path, "w") as f:
        f.write(page)
    print(f"[web] wrote {out_path}")
    return out_path


# =============================================================================
# PART 5 — DELIVERY #2: email (Gmail SMTP + app password).
# =============================================================================

def send_email(md):
    if not (GMAIL_ADDRESS and GMAIL_APP_PASSWORD and DIGEST_TO):
        print("[email] skipped — email secrets not set "
              "(GMAIL_ADDRESS / GMAIL_APP_PASSWORD).")
        return False

    msg = EmailMessage()
    msg["Subject"] = f"Morning Brief — {TODAY}"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = DIGEST_TO
    msg.set_content(md)  # plain-text fallback = the raw Markdown
    body_html = PAGE_TEMPLATE.format(
        body=md_to_html(md),
        stamp=datetime.datetime.now().strftime("%A, %d %B %Y at %H:%M"),
    )
    msg.add_alternative(body_html, subtype="html")

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print(f"[email] sent to {DIGEST_TO}")
        return True
    except Exception as e:
        print(f"[email] ERROR: {type(e).__name__}: {e}")
        return False


# =============================================================================
# PART 6 — A small EVAL: did the agent do the job? (Session 7 habit.)
# =============================================================================

def evaluate(md, hit_limit):
    checks = {
        "Finished within the step limit": not hit_limit,
        "Produced a non-empty brief": len(md.strip()) > 0,
        "Has a Top Story": "## Top Story" in md,
        "Has AI sections": "## AI" in md,
        "Has Markets sections": "## Markets" in md,
        "Includes clickable links": md.count("](") >= 3,
    }
    print("\n=== EVAL ===")
    passed = sum(1 for ok in checks.values() if ok)
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}")
    print(f"  ----> {passed}/{len(checks)} checks passed")
    return passed == len(checks)


# =============================================================================
# PART 7 — Wire it together: think → publish → email → check.
# =============================================================================

if __name__ == "__main__":
    print(f"=== Building your morning brief for {TODAY} ===\n")
    brief, steps_used, hit_limit, model_used = run_agent(TASK)

    print("\n=== BRIEF (Markdown) ===\n")
    print(brief)

    write_web_page(brief)   # channel 1: always
    send_email(brief)       # channel 2: only if secrets are set
    evaluate(brief, hit_limit)
