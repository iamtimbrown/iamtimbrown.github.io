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

### ▶️ Session 8 — Ship a useful agent (NEXT)
Something real, e.g. a morning digest agent that checks sources and emails a
summary. Deploy so it runs without the laptop.
Boardroom layer: full picture of what an AI build takes; RAG, evals,
fine-tuning vs. prompting folded in along the way.

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
