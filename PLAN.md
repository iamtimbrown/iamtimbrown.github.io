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

### ▶️ Session 3 — GitHub (NEXT)
Push the repo online. Free account at github.com.
Boardroom layer: repos as a team's source of truth; where code review and
deployment start.

### Session 4 — Deploy (GitHub Pages)
Turn the repo into a live site at timbrown.github.io. Real, shareable URL.
Boardroom layer: what "going live" involves; environments.

### Session 5 — Call Claude from code ⭐ the AI layer begins
Small Python script that calls the Claude API. Needs an API key (small cost,
pennies per call).
Boardroom layer: tokens, context windows, why AI COGS scale with usage.

### Session 6–7 — Build an agent (tool use)
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
