import anthropic
import os
from typing import List

def summarize_key_usage(events: List[str]) -> str:
    """
    Summarizes key usage and crypto events using Anthropic Claude.
    """
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    prompt = "Provide a concise summary of these key management and crypto events:\\n\\n" + "\\n".join(events)
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=300,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
