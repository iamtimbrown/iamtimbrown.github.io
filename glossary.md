# Tim's Tech & AI Glossary

Plain-English definitions, in roughly the order we met them. Updated each session.

---

## Session 1 — Running a website locally

**Terminal / command line** — The text-based way to control your computer. You type commands instead of clicking. Engineers live here because it's faster and scriptable.

**Command** — An instruction typed into Terminal, e.g. `cd`, `pwd`, `mkdir`.

**Directory** — Just the technical word for a folder. `cd` = "change directory" (move into a folder). `pwd` = "print working directory" (show where I am). `mkdir` = "make directory" (create a folder).

**HTML** — The language web page *content* is written in. Headings, paragraphs, links — all defined with tags like `<h1>` and `<a>`.

**CSS** — The language for how a page *looks*: colors, fonts, spacing. Lives alongside or inside the HTML.

**Server** — A program (and by extension, the machine running it) that waits for requests and responds — e.g. a web server sends back web pages. A "server" in a data center is just a computer that's always on, running server programs.

**localhost** — An address meaning "this machine." `localhost:8000` = "talk to the server running on my own computer." Not reachable by anyone else.

**Port** — A numbered channel on a machine that a server listens on (the `:8000` part). One machine can run many servers, each on a different port. Websites use port 443 (https) by default so you never see it.

**Deploy / ship** — To put software onto a server so it runs live for real users, rather than just on a developer's laptop. "When does it deploy?" = "when is it live?"

---

## Session 2 preview — Git & GitHub

**Git** — A tool that tracks every change ever made to a project's files. The universal standard for managing code.

**Repo (repository)** — A project folder being tracked by git, including its full change history. "It's in the repo" = "the code officially exists in our shared project."

**Commit** — One saved snapshot of the project, with a note about what changed. Projects accumulate thousands of commits; they're the project's paper trail.

**Push / pull** — Push = send your commits to the online copy (e.g. GitHub). Pull = fetch others' commits down to your machine. This is how teams stay in sync.

**GitHub** — The dominant website for hosting repos online. Backup, collaboration, and increasingly the hub where code review and deployment kick off.

---

## Coming up — the AI layer

**API** — A way for one program to use another program over the internet, machine-to-machine. AI products call a model provider's API. Commercially: API usage is metered, which drives AI cost structures.

**Token** — The unit AI models read and write text in (~¾ of a word). API pricing is per token, so tokens are the unit of AI COGS.

**Context window** — The maximum amount of text a model can consider at once. Limits how much background an AI can "hold in mind"; a key spec when comparing models.

**Agent** — An AI program that doesn't just answer, but takes actions: calling tools, checking results, looping until a task is done.

**Tool use / function calling** — The mechanism that lets a model trigger real actions (search the web, send an email) via functions a developer wrote. The building block of agents.

*(RAG, fine-tuning, evals, MCP — defined when we meet them.)*
