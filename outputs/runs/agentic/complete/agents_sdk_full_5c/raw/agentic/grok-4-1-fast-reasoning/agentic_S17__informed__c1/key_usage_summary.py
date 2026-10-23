import os
import json
from anthropic import Anthropic

def summarize_key_usage(events: list[dict]) -> str:
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    prompt = f"Summarize the following key usage and crypto events in a concise report:\\n\\n{json.dumps(events, indent=2)}"
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text