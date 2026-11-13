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

### ✅ Session 13 — A database (BUILT 12 Nov — Tim's hands-on part below)
Swapped signals-app/'s storage from one JSON file per profile to SQLite (signals.db, gitignored).
Pages, routes and the form are unchanged; only the layer underneath moved.
  - db.py — all the SQL. SCHEMA with 3 tables: users (slug UNIQUE, name, email [empty until
    Session 14], answers + config as JSON, created/updated, last_email_opened_at), user_locations
    (one row per person+place, so "who wants Singapore?" is a JOIN), leads_sent (user_id -> users
    ON DELETE CASCADE, sent_on, kind signal|role, company, trigger, url, fit_score; indexed by
    user+date). Functions: get/create/update/list/delete user, record_leads, recently_sent
    (30-day no-repeat), purge_old_leads (12-month retention), mark_email_opened. Each call runs
    as one transaction; foreign keys switched on.
  - app.py — storage functions now call db.py; a duplicate name is caught by the DB's UNIQUE rule
    even under a race. NEW route POST /p/<slug>/delete + "Delete profile" button (confirm box).
  - migrate.py — copies profiles/*.json into the DB (re-runnable; skips existing; JSON files kept
    as a backup).
  - test_app.py — 45 tests (31 old + 14 DB: tables, columns, the Singapore JOIN, UNIQUE, no-repeat
    window, retention purge, open tracking, delete via POST only, CASCADE).
Tim's privacy decisions (12 Nov): add the email column now; TRACK OPENS but disclose it openly;
keep lead history 12 MONTHS; deleting an account deletes EVERYTHING at once.
Concepts (glossary.md): database, SQLite vs Postgres, table/row/column, schema, primary + foreign
key, constraints, CASCADE, SQL verbs, JOIN, normalisation, transaction, index, parameterised
queries / SQL injection, data migration, retention, open tracking.
Still to do in Session 15: wire record_leads/recently_sent into the weekly job; build the tracking
pixel; write the privacy note (disclose open tracking, 12-month retention, delete-everything).

To run: cd ~/Documents/"Claude project"/signals-app  then  python3 migrate.py  (once), python3 app.py
Explore: sqlite3 signals.db   (then SQL; .quit to leave)
Tests:   python3 test_app.py

### ✅ Session 14 — User accounts (DONE 12 Nov)
Decided (Tim, 12 Nov): email MAGIC LINK + SIGN IN WITH LINKEDIN. Covers everyone; no passwords stored.
  - auth.py — the sign-in machinery. Magic link: 256-bit random token, only its SHA-256 HASH stored
    (login_tokens table), 15-minute expiry, single-use (atomic UPDATE), max 3 links per address per
    15 min. Email via the same Gmail app password as the Morning Brief (prints to the terminal if no
    Gmail settings, or EMAIL_MODE=print). Links built from APP_BASE_URL (never the request's Host
    header). LinkedIn = OpenID Connect: authorize -> code -> server swaps code + client secret for a
    token -> /v2/userinfo -> sign in ONLY if email_verified is true. Secrets: env vars first, then
    signals-app/secrets.env (gitignored), then the parent secrets.env (Gmail).
  - app.py — signed SESSION COOKIE (secret key in gitignored .secret_key; HttpOnly, SameSite=Lax,
    Secure once on HTTPS, 30 days). login_required (authentication) + own_profile (authorisation:
    someone else's profile = 404). CSRF token on every POST form. New routes: /login, /login/sent,
    /auth/magic/<token> (GET shows a Sign-in button because email scanners pre-open links; POST signs
    in), /auth/linkedin + callback (state check), /me, POST /logout. One person = one radar; same
    name for two people -> alex-chen-2. Home page no longer lists anyone's profiles. Delete = account
    deleted + signed out (sign-in links go too).
  - db.py — login_tokens table + functions; get_user_by_email, set_email; create_user takes email.
  - claim.py — attaches an email to a pre-accounts profile (Tim's own).
  - templates: login, login_sent, magic_confirm; account bar in base.html; CSRF fields in forms.
  - test_app.py — 86 tests (45 old, adapted + 41 new: sign-in, hashing, single-use, expiry, rate
    limit, no user enumeration, Host-header trick, cookie flags, CSRF, other people's profiles = 404,
    logout, LinkedIn state/verified-email/same-account, delete removes tokens).
Concepts (glossary.md): authentication vs authorisation, IDOR, sessions, cookies, secret key,
passwordless, hash, tokens, link scanners, user enumeration, rate limiting, CSRF, Host header
injection, session fixation, 404 vs 403, OAuth 2.0, OIDC, client ID/secret, redirect URI, state,
email_verified, identity provider / SSO, build-vs-buy auth.

TIM'S HANDS-ON (Session 14):
  1. Run the tests:      cd ~/Documents/"Claude project"/signals-app   then   python3 test_app.py
  2. Claim your profile: python3 claim.py tim-brown-global-and-apac-partnerships <your email>
  3. Sign in by email:   python3 app.py -> localhost:5050 -> Sign in -> email arrives (real Gmail) ->
     click -> Sign in button. Watch the terminal log: POST /login 302, GET /auth/magic 200, POST 302.
  4. Try to break it: click the same link twice; open a private window and visit your /p/... URL.
  5. LinkedIn: create an app at developer.linkedin.com (needs a LinkedIn Company Page to attach it to;
     can be a simple "Opportunity Radar" page), add the product "Sign In with LinkedIn using OpenID
     Connect", add redirect URL http://localhost:5050/auth/linkedin/callback, then put
     LINKEDIN_CLIENT_ID=... and LINKEDIN_CLIENT_SECRET=... in signals-app/secrets.env (TextEdit,
     plain text). Restart app.py -> the LinkedIn button appears.
  6. Commit: git add -A  then  git commit -m "Session 14: accounts (magic link + LinkedIn)"
DONE 12 Nov: Tim claimed his profile, signed in by email link (real Gmail), tested reuse (400),
private window (redirect to sign-in) and sign-out; committed. LinkedIn: Company Page "Opportunity
Radar" (linkedin.com/company/opportunity-radar-source; the plain URL was taken by another page,
so check the name before marketing it), developer app "Opportunity Radar" with the OIDC product,
redirect URL http://localhost:5050/auth/linkedin/callback, client ID + secret in
signals-app/secrets.env (gitignored). Signed in with LinkedIn: consent screen showed the logo +
name/photo/email. Logo: signals-app/static/radar-logo.png.
Still to do in Session 15 (deploy): HTTPS + APP_BASE_URL set to the real address (Secure cookies
switch on automatically), add the production redirect URL in LinkedIn, a privacy note.

### ▶️ NEXT: Session 15 — Deploy for others (full plan agreed 13 Nov)
Goal: 5 testers can sign in at a real https:// address, set up a radar, get a reviewed first briefing
straight away, then a Monday email each week. Two sittings, ~1.5-2h each.

KEY ARCHITECTURE DECISION (start of 15a): move SQLite -> hosted POSTGRES. On a hosting service the
web app and the weekly job run as separate machines; a SQLite file can live on only one of them.
A managed Postgres both can reach is the standard answer. db.py's SQL mostly carries over.

15a — GET IT ONLINE
  1. Decide: host (Render vs Railway — check current prices; avoid sleeping free tiers) + Postgres.
  2. Production-ready code: gunicorn (real web server), debug OFF, Postgres in db.py, settings from
     env vars, /healthz page. Tests updated and passing.
  3. Private GitHub repo for signals-app; push.
  4. Host: web service + Postgres; secrets in the host's settings (SIGNALS_SECRET_KEY, LinkedIn,
     Gmail, APP_BASE_URL). Deploy-on-push (CI/CD, like Session 4).
  5. Live https URL -> APP_BASE_URL; add live callback URL in LinkedIn (keep localhost one too).
  6. Privacy page: what we store, open tracking disclosed, 12-month retention, delete-everything,
     contact. Linked from footer + sign-in page; also LinkedIn app's privacy policy URL.
  7. Sample briefing on the landing page: 3 REAL leads Tim picks from a Radar run, labelled with
     the week, personal bits stripped.
  7a. NAME + DOMAIN (decided 13 Nov): no domain purchase for now — use the host's free address.
     Keep "Opportunity Radar". Revisit only if the trial shows real traction. Name research done:
     Vantage, Foresight, Exec/Executive Edge clash with exec-recruiting firms; "Signal Radar" was the
     cleanest, but signalradar.com is a A$14.6k premium and .io/.app/.dev are taken (check what's on
     them first). Cheaper later options: signalradar.ai/.co, getsignalradar.com, .com.au (needs ABN).
     Keep spend minimal throughout: this is a learning build first.
  7b. INVITE-ONLY (Tim, 13 Nov): an allowlist of invited emails (ALLOWED_EMAILS on the host). Anyone
     else who finds the URL can't create an account or trigger a ~US$2 briefing. Tim adds testers
     to the list only when 15b is done and checked.
  8. Smoke test: Tim signs in on his phone (email + LinkedIn); a second person signs in; check
     they can't see each other.
  CHECKPOINT: app live and shareable; no emails flowing yet.

15b — THE WEEKLY ENGINE FOR EVERY USER
  1. Engine adapter: radar.py runs from a user's config in the DB (not profile.json).
  2. Weekly job (host cron, Mondays 06:47 SGT): loop all users; one user failing doesn't stop
     the rest; per-user cost cap; run summary emailed to Tim.
  3. No-repeats: recently_sent() filters, record_leads() saves what was sent; purge_old_leads()
     monthly.
  4. Per-user email (ranked by fit, who-to-approach + angle, source links, in-play flag). Gmail
     SMTP is fine for 5 (limit ~500/day); note: a transactional email service (Resend/Postmark +
     SPF/DKIM) is the scale-up path.
  5. Open tracking pixel + disclosure line in each email.
  6. FIRST BRIEFING ON SIGN-UP: 30-day look-back; goes to Tim for approval first; "quiet week" honesty
     if few strong leads.
  7. Evals before inviting: dry-run 3-4 personas (e.g. Sydney sales leader, Singapore channel head,
     fintech partnerships director, Tim) and score against the landing-page promises.
  8. Go live with Tim as user #1 for one Monday, then invite testers.
  DONE = every landing-page promise checked off.

AI COST DECISION (Tim, 13 Nov): run the trial WEEKLY and do it well (~US$45/month for 5 users;
~US$80 first month incl. sign-up briefings + persona dry-runs). Build the cheap-model split (Haiku
filters, Sonnet writes) into 15b from the start. Other levers (shared searches across users,
fortnightly, fewer hunts) assessed only if it becomes ongoing — shared searches = Session 16 lesson.
Costs: hosting + Postgres ~US$10-25/month (confirm at 15a); AI ~US$2 per user per run -> ~US$40/month
for 5 testers + ~US$2 per sign-up briefing. Feeds Session 16 (pricing / unit economics).
Concepts: PaaS, production web server (WSGI/gunicorn), environment config, managed database /
Postgres, stateless app servers, health checks, CI/CD, background jobs / cron workers, multi-tenancy,
fault isolation, per-tenant cost caps, email deliverability (SPF/DKIM), privacy notice.

### ▶️ The Product Track: "full AI stack in practice" (Sessions 12+)
Shift of goal: Sessions 1-11 built agents that serve ME. The product track builds a small real
SaaS product that OTHER people log into and pay for — the layer around the AI that real products
need. Practice product: an "early signals" intelligence app (who's raising, entering a market or
appointing a regional head), reusing the Radar engine so the new learning is everything around it.
Each session still ends with something working + the boardroom layer.

  12. A real web app — pages + a form to describe what you're looking for (replaces hand-editing
      a JSON config). Concepts: frontend vs backend, routes, HTTP, web frameworks.
  13. A database — store each user's profile and results. Concepts: tables, SQL, schema.
  14. User accounts — sign-up/login, passwords done properly, "Sign in with Google".
      Concepts: authentication vs authorisation, sessions, OAuth, security basics.
  15. Deploy for others — hosted app, real URL, a weekly job per user. Concepts: PaaS hosting,
      background workers, multi-tenancy.
  16. Payments — Stripe subscriptions in test mode. Concepts: billing, webhooks, unit economics
      (AI COGS ~$2/user/week -> what must it cost?).
  17. Run it reliably — monitoring, alerts, per-user cost caps, privacy. Concepts: observability,
      SLAs, data protection (Australian Privacy Act).
  18. Five real users — feedback, usage, pricing test. Concepts: product-market fit, retention.
Roughly 8-12 sessions. Optional side quest first: a short Radar tuning pass (see private notes).

### ✅ Session 12 — A real web app (DONE 11 Nov)
Built signals-app/ — "Early Signals", a Flask web app (gitignored here; own private repo in
Session 15). Pages + a form to describe what you're looking for; saving it writes the SAME config
shape radar.py reads, so the engine is unchanged. Routes: GET / (profiles), GET+POST /new (form),
GET /p/<slug> (view + "under the hood" config), GET+POST /p/<slug>/edit, GET /p/<slug>.json (API).
  - app.py — the BACKEND: form choices as config (locations -> match keywords, seniority levels,
    5 signal-hunt templates filled with each user's places + sectors), validate(), build_config(),
    storage = one JSON file per profile in profiles/ (crude on purpose — Session 13 = database).
  - templates/ (base, index, form, view, 404) + static/style.css — the FRONTEND (Jinja templates).
  - test_app.py — 26 tests with Flask's test client: pages, validation (400 + answers kept),
    POST -> redirect -> GET, edit, the JSON API, security (path tricks, HTML escaping), and
    ENGINE COMPATIBILITY: radar.py's own prompt + filters run on the form's output.
Key concepts: frontend vs backend, HTTP (request/response, GET vs POST, status codes 200/302/
400/404), routes, web framework (Flask), templates, form validation ("never trust the browser"),
POST-redirect-GET, API = same data without the HTML, debug mode. All in glossary.md.

To run: cd ~/Documents/"Claude project"/signals-app
        pip3 install flask        (once)
        python3 app.py            then open http://localhost:5050   (Ctrl+C to stop)
Tests:  python3 test_app.py
Port 5050, not 5000: macOS AirPlay Receiver squats on 5000.
Done 11 Nov: Tim ran it, saved his own profile, watched the HTTP log (200/302/304/400/404), tried
the <script> test, ran the tests, made signals-app/'s first commit. Role types updated to drop
"alliances"/GSI and add AI-stack partnerships. Lesson: the public repo gets daily robot commits
(Morning Brief), so `git pull --rebase` before `git push`.
NEXT (before Session 13): Tim reviews the form critically, as if he were one of the 5 test users.
  Start it: cd ~/Documents/"Claude project"/signals-app  then  python3 app.py  -> localhost:5050
  Ask: is each question clear to a stranger? anything missing? anything unnecessary? do the options
  fit? does "What the engine will hunt for" describe what you'd actually want found? Also: which of
  the 4 possible customer groups is it for (job seekers, recruiters, vendor sales/partnership people,
  investors)? — that choice shapes the questions. Bring notes; Claude makes the changes.
  How Tim wants sessions run: start each with WHAT we're building, WHY, and WHAT TO WATCH FOR.
FORM REVIEW DONE (12 Nov) — Tim reviewed it as a tester would. Changes: "New radar profile"; "Your
  background" with paste-your-LinkedIn/CV hint, 100-300 word guide, live word counter (first frontend JS),
  400-word cap enforced in the backend; locations widened to all APAC, grouped by sub-region with
  "All of ..." buttons; role types expanded + grouped (channel, strategic accounts/CS, solutions/pre-sales,
  strategy/corp dev) with old names mapped so saved profiles still open; sectors split into TWO questions
  (what the company sells / which industries it serves + "anything more specific"); "Pivotal partnerships
  that create new opportunities" (display labels now separate from engine hunt names); "Which early
  signals matter to you?"; generic example text. Visual: executive navy/teal theme + original radar mark,
  slow sweep animation, styled content boxes. Tests: 31.
  Signal labels now match the home page (done 12 Nov).
REMINDER for Tim: on your own radar profile (Edit), move "Thailand" to the Bangkok tick box, tick your
  tech-company types + Financial services, then save.
THEN: Session 13 — a database.
LANDING PAGE (12 Nov): app renamed "Opportunity Radar"; home page now carries Tim's value proposition
  (headline "See the opening before it's advertised", What it watches for / What you get / How it works).
  Target customer chosen: senior job seekers. The page describes the FINISHED product — its promises are
  the acceptance checklist before inviting the 5 testers: weekly Monday email per user, ranked by fit;
  who-to-approach + fit angle per lead; strict role filter; source-checked; 30-day no-repeat + in-play
  flag; profile edits flow into the next email (Sessions 13-15 must deliver these).
  FEATURE TO ADD (tuning pass): a TRUSTED-SOURCES list — have the Radar favour named outlets per market
  (e.g. AFR, DealStreetAsia, Business Wire/GlobeNewswire, Seek, MyCareersFuture) via web_search's
  allowed/priority domains, so the landing page can honestly name them. Watch: paywalled outlets
  may only yield snippets; measure hit rate on a dry run before promising any outlet by name.

### Other options (later)
RAG and MCP can slot into the product track later. RAG in practice — best done on business documents, for interview credibility (personal RAG
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
