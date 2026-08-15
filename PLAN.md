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

### ▶️ Session 6–7 — Build an agent (tool use) (NEXT)
Give the model tools it can call (fetch a webpage, read a file) and watch it
loop until a task is done.
Boardroom layer: what "agentic" means mechanically; demo vs. product;
reliability as the hard part.

### Session 8 — Ship a useful agent
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
