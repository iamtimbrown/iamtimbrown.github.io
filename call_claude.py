"""
call_claude.py — Session 5: our first call to the Claude API from code.

What this does, in plain terms:
  1. Reads the API key from an environment variable (NOT written in this file,
     so it's safe to commit to git / push to GitHub).
  2. Sends one message to a Claude model over the API.
  3. Prints Claude's reply.
  4. Prints how many tokens the call used — the unit AI is billed in.
"""

import os
from anthropic import Anthropic

# Where does the key come from? We read it from a file called key.txt that
# sits next to this script. key.txt is listed in .gitignore, so git ignores
# it and it never gets committed or pushed to GitHub. This is the standard
# real-world pattern: secrets live in a gitignored file, never in the code.
#
# .strip() removes any stray spaces or newlines around the key — a common
# cause of "invalid x-api-key" errors.
here = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(here, "key.txt")

if not os.path.exists(key_path):
    raise SystemExit(
        "No key.txt found. Create it by copying your key in the Console, then:\n"
        "  pbpaste > key.txt"
    )

with open(key_path) as f:
    api_key = f.read().strip()

# This 'client' object is our connection to the API. We hand it the key.
client = Anthropic(api_key=api_key)

# Here's the actual API call. Three things we're specifying:
#   model      — which Claude to use. Haiku is the fastest/cheapest, good for
#                a hello-world. Swap for "claude-sonnet-5" for a smarter answer.
#   max_tokens — a ceiling on how long the reply can be. A safety cap on cost:
#                the model can't run away and generate (and bill) forever.
#   messages   — the conversation. One message from us, role "user".
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=300,
    messages=[
        {
            "role": "user",
            "content": "In two sentences, explain what an API is to a "
                       "business executive who is not technical.",
        }
    ],
)

# The reply text lives in response.content[0].text
print("\n=== Claude's reply ===\n")
print(response.content[0].text)

# The 'usage' field is the meter reading for THIS call. input_tokens = what we
# sent (our prompt), output_tokens = what Claude wrote back. Add them up and
# multiply by the model's per-token price and you get the cost of this call.
# This is AI COGS in miniature: every call is metered, every token has a price.
print("\n=== Token usage (the meter) ===")
print(f"Input tokens (what we sent):     {response.usage.input_tokens}")
print(f"Output tokens (what Claude wrote): {response.usage.output_tokens}")
