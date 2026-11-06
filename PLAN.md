# Tim's Learning Plan — AI Commercial Leader Track

**Goal:** Become a technically strong AI commercial leader who understands
conceptually how things get built — differentiated from simple GenAI users.

**Method:** Learn by building. Each session ends with something working, plus
the "boardroom layer" — the concepts, trade-offs, and cost implications.
All jargon gets defined in glossary.md as we go.

**How to resume:** In a new Claude conversation, say:
"Read PLAN.md in my Claude project folder and continue where we left off."

---

## Roadmap & status

### ✅ Session 1 — Run a website locally (DONE)
Built index.html, served it with `python3 -m http.server 8000`, viewed at
localhost:8000, edited with TextEdit, learned the edit → save → refresh loop.
Key concepts: terminal, localhost, ports, what a server actually is.

### ✅ Session 2 — Git (DONE)
Turned the project into a git repo (`git init`) and learned the snapshot loop:
edit → `git status` → `git diff` → `git add` → `git commit`. Made two commits
(initial commit of all three files; then a fix to a broken SMH link). Read
history with `git log --oneline`. Set global name/email for commits.
Key concepts: repo, commit, staging, diff, HEAD/branch, main.

### ✅ Session 3 — GitHub (DONE)
Pushed the repo online. Created a free github.com account (username:
iamtimbrown), made an empty public repo named `iamtimbrown.github.io`,
connected it with `git remote add origin`, and pushed with `git push -u origin
main`. Hit the auth wall (passwords no longer work) and generated a personal
access token to authenticate. Repo now lives at
github.com/iamtimbrown/iamtimbrown.github.io.
Key concepts: remote, origin, push/pull, personal access token, source of truth.

### ✅ Session 4 — Deploy (GitHub Pages) (DONE)
Confirmed the site is live at https://iamtimbrown.github.io — a real, shareable
URL serving the homepage (verified it loads; SMH link works). Pages was already
enabled (source: main / root); the Save button was greyed out because nothing
needed changing. Learned that the Session 3 `git push` auto-triggered the deploy.
Key concepts: going live (localhost vs. public), environments (dev/staging/prod),
CI/CD (a push to main auto-builds and publishes).

### ✅ Session 5 — Call Claude from code ⭐ the AI layer begins (DONE)
Wrote call_claude.py — a Python script that calls the Claude API and prints the
reply plus token usage. Set up a Console account with $5 credit, generated an
API key, installed the anthropic SDK (pip3). First call succeeded: sent a prompt
about "what is an API," got a reply back, used 25 input + 78 output tokens.
Key handling: key lives in key.txt, which is gitignored (secrets never in code).
Learned the hard way that the clipboard is a single slot — copying commands and
copying the key clobber each other; TextEdit (plain text) is the reliable way to
get a key into a file.
Boardroom layer: tokens are the billing unit (in + out × per-model price); AI
COGS scale with usage (unlike normal software); model choice (Haiku vs Opus) is a
cost lever; context window caps tokens-per-call.

To run again: cd ~/Documents/"Claude project" then python3 call_claude.py
(the script reads the key from key.txt automatically — no read/export needed).

TODO next session: delete the leftover "key . txt.rtf" file (it holds the key;
gitignored so safe, but trash it for tidiness). Consider making the key a
permanent env var later instead of a file.

### ✅ Session 6 — Build an agent (tool use) ⭐ agents begin (DONE)
Wrote agent.py — our first agent. Gave the Haiku model two tools (read_file,
fetch_url) and a goal: "compare my live homepage to my local index.html." The
model decided on its own to fetch the live page, read the local file, then
compare — we never scripted the order. Saw the loop print step by step:
model → tool call → result → model, until stop_reason flipped from "tool_use"
to "end_turn".
Key mechanics: the agent LOOP (a messages list we call the model against
repeatedly), tool definitions (name + description + input_schema — the
description is how the model decides when to use a tool), and the
tool_use / tool_result pair that carries each step (matched by id).
Boardroom layer: "agentic" is just that loop, no magic. Demo vs. product —
making it work ONCE is easy, making it reliable on messy inputs is the whole
job (guardrails, step limits, permissions, evals). And agents multiply token
cost: each loop step is a separate metered call, and tool outputs re-enter as
input tokens — so step limits and cheap-model routing are cost levers.

To run: cd ~/Documents/"Claude project" then python3 agent.py

### ✅ Session 7 — Make the agent reliable (guardrails + evals) (DONE)
Hardened agent.py into agent2.py — same loop, made trustworthy. Added: a STEP
LIMIT (while step < MAX_STEPS = 8) so it can never loop forever; DEFENSIVE tools
that catch errors and return an "ERROR:" string fed back to the model, so a
broken source doesn't crash the run; and output TRIMMING (4000 chars) to keep
token cost bounded. Gave it a real task — summarise 3 web sources where one URL
is deliberately broken — and it degraded gracefully (summarised the 2 that
worked, flagged the 1 that failed). Then wrote a first EVAL: 3 automatic PASS/
FAIL checks on the run (finished within limit? produced an answer? flagged the
dead source?). Verified the guardrails with mocks before running.
Boardroom layer: demo→product = reliability engineering; guardrails contain a
model you don't fully trust; evals let you say "reliable" with a number, and
they gate shipping. LLM-as-judge = the scalable eval grader (noted for later).

To run: cd ~/Documents/"Claude project" then python3 agent2.py
(agent.py, the Session 6 demo, is kept alongside for comparison — git diff them.)

### 📚 Side thread (during Session 6) — AI infrastructure economics
Sparked by a role description phrase: "GPU capacity, inferencing costs, model
deployment architectures." Worked it all the way down the stack. Everything is
written up in glossary.md (sections: infra economics; RAG vs. fine-tuning;
self-hosting & open vs. closed; the infrastructure stack). Visual companion:
ai-infrastructure-stack.html (also published as a Claude artifact). Covers:
inference vs. training, GPU capacity, deployment architectures, build-vs-buy =
cloud-vs-on-prem, sovereign cloud spectrum, open-weight vs. closed + weights,
neoclouds (own GPUs, colo not concrete, debt/circular financing), colocation
operators + PE ownership, and power as the binding constraint.

### ✅ Session 8 — Ship a useful agent (deploy on a schedule) (DONE)
Built digest.py — a morning-brief agent that fetches 7 RSS feeds (AI + markets,
tuned to Tim's holdings: big tech, semis, storage/memory), has Sonnet write a
structured brief (Top Story + AI Research/Business/Policy + Markets Holdings/Macro,
with clickable links), and DELIVERS it two ways: writes digest.html (published at
iamtimbrown.github.io/digest.html) and emails it via Gmail SMTP. Same agent loop +
guardrails as agent2.py, plus a model fallback (Sonnet -> Haiku). Then DEPLOYED it
on GitHub Actions (.github/workflows/digest.yml): runs daily at 07:00 SGT
(cron "0 23 * * *" in UTC) on GitHub's servers, laptop closed, and auto-commits the
new digest.html back to the repo. Secrets (API key, Gmail app password) live in
GitHub Secrets; locally in gitignored key.txt / secrets.env.
Key concepts: deployment, environment variables, secrets management, app passwords +
token scopes (least privilege), SMTP, cron, GitHub Actions (workflow/runner/triggers/
permissions), YAML, RSS + source diversity, model choice as cost lever + fallback,
"works on my machine" (env/secret parity). All defined in glossary.md.
Debugged live (both great lessons): the PAT needed the `workflow` scope before it
could push the workflow file; and the first cloud run 401'd because the API-key
secret had a stray character — re-pasted cleanly, then went green.

To run locally: cd ~/Documents/"Claude project" then python3 digest.py
To run in the cloud on demand: GitHub -> Actions -> Morning Brief -> Run workflow.

HOUSEKEEPING: Tim's Anthropic API key appeared in screenshots during this session —
consider rotating it (generate a new key in the Console, update key.txt AND the
ANTHROPIC_API_KEY GitHub secret, delete the old key). Not urgent, doesn't affect
anything working now.

### ✅ Session 9 — Build a discovery agent (the Scout) (DONE)
Built scout.py — an AI-ecosystem SCOUT that DISCOVERS rather than summarises. Reads
the thesis + companies already tracked (watchlist.json: 24 starter names across 7
stack layers), searches the live web via Anthropic's built-in web_search tool (biased
to Australia/APAC with user_location), judges what fits and isn't already tracked, and
proposes new companies for approval (a/s/q each). Approved ones are WRITTEN BACK into
watchlist.json — the agent edits its own state. First run: 6 web searches -> 10 real
candidates, 9 kept, heavily Australian (Heidi Health, Lyrebird, Lorikeet, Neara,
BrainChip, Q-CTRL, Appen, Andromeda Robotics, Groq). Watchlist now 33.
Key concepts: Monitor vs Scout, web search as a (server-side) tool, LLM-as-filter,
persistent state (read + write), human-in-the-loop approval, config-vs-engine
separation. All defined in glossary.md.

Resolved at session start (good ops lessons): the daily digest had been silently
FAILING since Oct 17. Root cause was the Anthropic API KEY EXPIRING on Oct 17 (not
credit — the 401 "invalid x-api-key" gave it away). Fixed by minting a new NON-EXPIRING
key and updating the GitHub secret; also topped credit $0.01 -> $35 and enabled
auto-reload so it can't silently die again. New machine (MacBook Air): installed Xcode
command-line tools + the anthropic SDK, put a fresh local key in key.txt.

To run: cd ~/Documents/"Claude project" then python3 scout.py
Files: scout.py (agent), watchlist.json (its state), proposals.json (last run's raw output).

TODO: tracker files (scout.py, watchlist.json) not yet committed/pushed to GitHub —
the local PAT (Session-3 token) expired and needs regenerating first. Not blocking;
Scout runs fine locally.

### ✅ Session 10 — Make the tracker self-running (DONE)
Built ai-tracker/ — its own folder AND its own PRIVATE GitHub repo (the website repo
is public; the watchlist holds private notes; parent .gitignore excludes it).
  - tracker.py — the weekly robot. MONITOR: checks the watchlist in batches of 6 via
    web_search, keeps only material news from the last 7 days (guardrails drop
    off-list / undated / out-of-window / sourceless items), de-dupes against
    monitor_state.json. SCOUT: proposes 5 new names, parks them in pending.json (never
    auto-adds; skips nothing already tracked, pending or rejected). Sends ONE email:
    "What moved" + "New candidates" + health check + run cost. Exits 1 on failure so
    GitHub flags it red. `--dry-run` = no email, no state saved.
  - approve.py — Tim's half: git pull, then a/s/l/q each pending candidate (a -> watchlist,
    s -> "rejected" forever, l -> stays pending), then commits + pushes.
  - scout.py, watchlist.json, proposals.json moved in here; scout.py patched to find
    key.txt / secrets.env in the parent folder.
  - .github/workflows/tracker.yml — Mondays 07:00 SGT (cron "0 23 * * 0" UTC), commits
    its state files back. Secrets needed in the NEW repo: ANTHROPIC_API_KEY,
    GMAIL_ADDRESS, GMAIL_APP_PASSWORD, (optional) TRACKER_TO.
Tested all guardrails with mocks (pause_turn, old/off-list/sourceless news, parse failure,
crashed batch, de-dupe across runs, reject memory). Local git repo initialised + files staged.

Dry runs: #1 $1.69 (6 of 17 weak/wrong sources) -> fixes -> #3 $2.03, 16 items all article-sourced. Fixes: source-quality check + a "second look" sub-editor that re-searches weak-linked items and keeps only verified ones (dropped ones listed in the email); one shared date window w/ 2-day grace; partnerships count for both parties; scout drops subsidiaries of tracked cos in code; added "layoffs or restructuring" signal.
DEPLOYED 5 Nov 2026: new PAT ("laptop push nov-2026", classic, repo+workflow, 90 days —
expires ~3 Feb 2027, regenerate before then); private repo github.com/iamtimbrown/ai-tracker
with 3 secrets (ANTHROPIC_API_KEY, GMAIL_ADDRESS, GMAIL_APP_PASSWORD); pushed; first manual
cloud run went green and the email arrived. Now runs every Monday 07:00 SGT on its own.
Each cloud run commits its state back, so on the laptop always `git pull` before editing
(approve.py does this automatically).

Tidy-ups 6 Nov: Anthropic key ROTATED (new non-expiring key "nov-2026" in key.txt and in both
repos' ANTHROPIC_API_KEY secret; old "digest" key + two expired keys deleted; verified locally
and via a manual Morning Brief run). Both schedules moved off the hour to 06:47 SGT (GitHub was
delaying 7:00 runs to 10-11am). git identity set on the MacBook. Still to do: review the 5
waiting candidates with approve.py.

To run: cd ~/Documents/"Claude project"/ai-tracker then python3 tracker.py --dry-run
Approve candidates: python3 approve.py (same folder)

### ✅ Session 11 — the Opportunity Radar (DONE)
A weekly agent built on the Session 10 tracker (schedule, email, fact-check, de-dupe memory).
Built + DEPLOYED 6 Nov 2026 in its own private repo (opportunity-radar/, gitignored here); runs
Mondays 07:17 SGT. Status,
deploy steps and the parallel "Reinvention" track are in PRIVATE_NOTES.md — kept out of git
because this repo is public. Read that file at the start of the next session.
New concepts: config-driven hunts, fit scoring with code-enforced thresholds, deterministic
filters after the LLM, entity-level de-dupe (company + trigger, not just URL).

✅ Model migration done 6 Nov: digest.py, scout.py (and so tracker.py) moved from
claude-sonnet-4-5 (end-of-life 30 Nov 2026) to claude-sonnet-5-5; tested and pushed in both repos.

### Other options (later)
RAG in practice — best done on business documents, for interview credibility (personal RAG
over CVs judged low value: the CV and pitches already exist). MCP. Refine the investment digest.

### Later / optional
- Richer redesign of the homepage (Claude builds it, Tim ships it)
- VPS session: rent a small server, SSH in, nginx — the manual way
- Custom domain (e.g. timbrown.com, ~$15/yr)

---

## Working notes

- Project folder: ~/Documents/Claude project (note the space — quote it in
  Terminal: `cd ~/Documents/"Claude project"`)
- Folder is in Documents, which may sync to iCloud — consider moving to
  ~/code before the git session gets serious.
- Restart local site anytime:
  `cd ~/Documents/"Claude project"` then `python3 -m http.server 8000`
- TextEdit is set to show HTML as code (Settings → Open and Save).
- Organization system: one chat per session, named clearly; durable stuff
  lives in files here, not in threads; update this file at end of each session.
