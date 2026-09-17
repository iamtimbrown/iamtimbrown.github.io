"""
agent2.py — Session 7: turning the agent from a DEMO into something RELIABLE.

agent.py (Session 6) worked because everything went right: the site was up, the
file was there, the model behaved. A real product can't assume that. This
version keeps the exact same loop but adds the guardrails that separate a demo
from something you'd actually ship:

  1. A STEP LIMIT  — the loop can never run forever (runaway loops = runaway $$).
  2. ERROR HANDLING — when a tool breaks, the error is handed BACK to the model
                      so it can recover or report honestly, instead of crashing.
  3. A USEFUL TASK  — summarise several real web pages. One URL is deliberately
                      broken, so you can watch the agent degrade gracefully.
  4. AN EVAL        — after the run, an automatic check that the agent actually
                      did the job. This is reliability made measurable.

Run it:  cd ~/Documents/"Claude project"  then  python3 agent2.py
"""

import os
import urllib.request
from anthropic import Anthropic

# --- Key handling: identical to Session 5/6 (gitignored key.txt) -------------
here = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(here, "key.txt")
if not os.path.exists(key_path):
    raise SystemExit("No key.txt found next to this script (see Session 5).")
with open(key_path) as f:
    api_key = f.read().strip()

client = Anthropic(api_key=api_key)


# =============================================================================
# PART 1 — Tools, now written DEFENSIVELY.
#
# The key change from Session 6: a tool must NEVER crash the whole program. If
# something goes wrong (site down, bad URL, missing file), we catch it and
# return a plain-text "ERROR: ..." string. That string gets fed back to the
# model as the tool's result — so the model *sees* the failure and can decide
# what to do (skip that source, try again, or tell the user honestly). A crash
# would kill the agent; a returned error keeps it in control.
# =============================================================================

def fetch_url(url):
    """Download a web page and return its text — or an ERROR string if it fails."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "tim-agent"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        # Trim: a full page can be huge, and every character we feed back becomes
        # input tokens on the NEXT call (i.e. money). 4000 chars is plenty here.
        return text[:4000]
    except Exception as e:
        return f"ERROR: could not fetch {url} ({type(e).__name__}: {e})"


def read_file(path):
    """Read a local file — or return an ERROR string if it isn't there."""
    try:
        with open(os.path.join(here, path)) as fh:
            return fh.read()
    except Exception as e:
        return f"ERROR: could not read {path} ({type(e).__name__}: {e})"


TOOL_FUNCTIONS = {"fetch_url": fetch_url, "read_file": read_file}

TOOLS = [
    {
        "name": "fetch_url",
        "description": "Download a web page over the internet and return its text. "
                       "If it fails, it returns a string starting with 'ERROR:' — "
                       "treat that as a failed source, not a reason to stop.",
        "input_schema": {
            "type": "object",
            "properties": {"url": {"type": "string", "description": "Full URL to fetch."}},
            "required": ["url"],
        },
    },
    {
        "name": "read_file",
        "description": "Read a text file from the project folder and return its contents. "
                       "Returns an 'ERROR:' string if the file is missing.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Filename, e.g. 'index.html'."}},
            "required": ["path"],
        },
    },
]


# =============================================================================
# PART 2 — The agent loop, now with a STEP LIMIT.
#
# The only structural change from Session 6 is `while step < MAX_STEPS`. In the
# demo, `while True` was fine because we trusted the model to finish. In
# production you never do: a confused model can loop forever, and every loop is
# a paid API call. MAX_STEPS is a hard ceiling — a circuit breaker. If the agent
# hasn't finished by then, we stop it ourselves and say so, rather than letting
# it burn tokens indefinitely.
# =============================================================================

MAX_STEPS = 8   # the circuit breaker: never more than 8 model calls per run.

TASK = (
    "Give me a short briefing on what 'example.com' is and why it exists. "
    "Check these three sources, then write 3 bullet points, and finish with a "
    "line naming any source you could NOT read:\n"
    "  1. https://example.com\n"
    "  2. https://www.iana.org/help/example-domains\n"
    "  3. https://no-such-site-9f8a7b6c.invalid\n"
    "Do not give up just because one source fails."
)


def run_agent(task):
    """Run the loop. Returns (final_text, steps_used, hit_limit)."""
    messages = [{"role": "user", "content": task}]
    print("=== TASK ===")
    print(task, "\n")

    step = 0
    final_text = ""
    while step < MAX_STEPS:
        step += 1
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "text":
                    print(f"[step {step}] thinks: {block.text.strip()}")
                elif block.type == "tool_use":
                    print(f"[step {step}] calls: {block.name}({block.input})")
                    output = TOOL_FUNCTIONS[block.name](**block.input)
                    flag = "  <-- ERROR returned" if output.startswith("ERROR:") else ""
                    print(f"[step {step}] result: {len(output)} chars{flag}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": output,
                    })
            messages.append({"role": "user", "content": tool_results})
            continue

        # end_turn: the agent is done.
        for block in response.content:
            if block.type == "text":
                final_text += block.text
        print("\n=== FINAL ANSWER ===")
        print(final_text)
        print(f"\n(Finished in {step} model calls.)")
        return final_text, step, False

    # If we fall out of the while, we hit the ceiling without finishing.
    print(f"\n!! STEP LIMIT ({MAX_STEPS}) REACHED — stopped the agent before it "
          f"could loop further. In production this would alert someone.")
    return final_text, step, True


# =============================================================================
# PART 3 — A first EVAL.
#
# "Evals" = automatic tests for an AI system. A demo you eyeball once; a product
# you check the same way every time, so you notice the day it breaks. Below is a
# tiny eval: three concrete checks on the run. Real eval suites run dozens or
# hundreds of cases like this and score them — but the idea is exactly this.
#
# Note the third check uses simple keyword matching. That's crude; the scalable
# version is "LLM-as-judge" — asking a model to grade the output against a
# rubric. Same spirit, more flexible. We'll meet that later.
# =============================================================================

def evaluate(final_text, steps_used, hit_limit):
    text = final_text.lower()
    checks = {
        "Finished without hitting the step limit":
            not hit_limit,
        "Produced a non-empty answer":
            len(final_text.strip()) > 0,
        "Explained what example.com is (mentions 'example' + 'document/reserved')":
            "example" in text and ("document" in text or "reserv" in text or "illustrat" in text),
        "Honestly flagged the unreachable source":
            "invalid" in text or "could not" in text or "couldn't" in text or "unable" in text,
    }
    print("\n=== EVAL ===")
    passed = 0
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}")
        passed += 1 if ok else 0
    print(f"  ----> {passed}/{len(checks)} checks passed")
    return passed == len(checks)


if __name__ == "__main__":
    final_text, steps_used, hit_limit = run_agent(TASK)
    evaluate(final_text, steps_used, hit_limit)
