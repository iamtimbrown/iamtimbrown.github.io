"""
agent.py — Session 6: our first AGENT (tool use).

The big shift from Session 5:
  In Session 5 we sent Claude a question and it sent back an answer. One shot.
  A model on its own can only produce text — it can't look anything up, open a
  file, or check a website.

  An AGENT is different. We hand the model a set of TOOLS (little functions we
  wrote), and instead of just answering, the model can say "run this tool for
  me." Our code runs it, hands back the result, and the model decides what to do
  next — call another tool, or give the final answer. That back-and-forth is
  "the loop," and it's the entire mechanical secret behind the word "agentic."

  Today's task for the agent:
    "Compare my live homepage (https://iamtimbrown.github.io) with my local
     index.html file. Are they the same? If not, what's different?"

  Notice the agent has to DO things to answer this: fetch a web page AND read a
  file off the disk. It'll use both tools, in whatever order it decides, then
  reason about what it found. We just watch.
"""

import os
import urllib.request
from anthropic import Anthropic

# --- Same key handling as Session 5: read it from the gitignored key.txt ------
here = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(here, "key.txt")
if not os.path.exists(key_path):
    raise SystemExit("No key.txt found next to this script (see Session 5).")
with open(key_path) as f:
    api_key = f.read().strip()

client = Anthropic(api_key=api_key)


# =============================================================================
# PART 1 — The tools, as plain Python functions.
#
# A "tool" is nothing exotic: it's just a normal function WE write and control.
# The model never runs code itself — it can only ASK us to run one of these, by
# name, with arguments. We stay in charge of what actually happens.
# =============================================================================

def read_file(path):
    """Read a text file from the local disk and return its contents."""
    full = os.path.join(here, path)          # look next to this script
    with open(full) as fh:
        return fh.read()


def fetch_url(url):
    """Download a web page and return its raw HTML as text."""
    req = urllib.request.Request(url, headers={"User-Agent": "tim-agent"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


# This dict lets us look up the real function by the name the model uses.
TOOL_FUNCTIONS = {
    "read_file": read_file,
    "fetch_url": fetch_url,
}


# =============================================================================
# PART 2 — Describe those tools to the model.
#
# The model can't see our Python. We have to DESCRIBE each tool in a structured
# way: its name, what it's for (the description — this is how the model decides
# WHEN to use it), and what arguments it takes. Good descriptions are half the
# job of building a reliable agent.
# =============================================================================

TOOLS = [
    {
        "name": "read_file",
        "description": "Read a text file that sits in the project folder and "
                       "return its contents. Use this to inspect local files "
                       "like index.html.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Filename to read, e.g. 'index.html'.",
                }
            },
            "required": ["path"],
        },
    },
    {
        "name": "fetch_url",
        "description": "Download a web page over the internet and return its "
                       "raw HTML. Use this to see what a live website is "
                       "actually serving.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Full URL to fetch, e.g. "
                                   "'https://iamtimbrown.github.io'.",
                }
            },
            "required": ["url"],
        },
    },
]


# =============================================================================
# PART 3 — The agent loop.
#
# This is the heart of it. We keep a running list of `messages` (the whole
# conversation so far) and call the model over and over:
#
#   - If the model returns a final text answer  -> we're done, print it.
#   - If the model asks to use a tool           -> we run it, add the result to
#                                                   the conversation, and loop
#                                                   again so the model can react.
#
# The model itself decides how many steps it needs. We never told it "fetch,
# then read, then compare" — we just gave it a goal and two tools. That autonomy
# is exactly what makes this an agent and not a script.
# =============================================================================

TASK = (
    "Compare my live homepage at https://iamtimbrown.github.io with my local "
    "index.html file. Fetch the live page, read the local file, and tell me "
    "whether they are identical. If they differ, summarise what's different."
)

messages = [{"role": "user", "content": TASK}]

print("=== TASK GIVEN TO THE AGENT ===")
print(TASK, "\n")

step = 0
while True:
    step += 1

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",   # same cheap model as Session 5
        max_tokens=1024,
        tools=TOOLS,                          # <-- the only new ingredient
        messages=messages,
    )

    # stop_reason tells us WHY the model stopped talking this turn.
    #   "tool_use" -> it wants us to run a tool before it continues.
    #   "end_turn" -> it's finished and gave a final answer.
    if response.stop_reason == "tool_use":
        # The model's turn can contain reasoning text AND one or more tool
        # requests. We must add the model's whole turn to the transcript first.
        messages.append({"role": "assistant", "content": response.content})

        # Now run every tool the model asked for and collect the results.
        tool_results = []
        for block in response.content:
            if block.type == "text":
                print(f"[step {step}] agent thinks: {block.text.strip()}")
            elif block.type == "tool_use":
                name = block.name
                args = block.input
                print(f"[step {step}] agent calls: {name}({args})")

                try:
                    output = TOOL_FUNCTIONS[name](**args)
                except Exception as e:
                    output = f"ERROR running {name}: {e}"

                # Trim huge outputs so we don't burn tokens (and money) needlessly.
                preview = output[:200].replace("\n", " ")
                print(f"[step {step}] tool returned {len(output)} chars: "
                      f"{preview}...\n")

                # Hand the result back to the model, tagged with the id it used.
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })

        # Feed all the tool results back in as the "user" turn, then loop.
        messages.append({"role": "user", "content": tool_results})
        continue

    # If we got here, stop_reason was "end_turn": the agent is done.
    print("=== FINAL ANSWER FROM THE AGENT ===")
    for block in response.content:
        if block.type == "text":
            print(block.text)
    print(f"\n(The agent finished in {step} model calls.)")
    break
