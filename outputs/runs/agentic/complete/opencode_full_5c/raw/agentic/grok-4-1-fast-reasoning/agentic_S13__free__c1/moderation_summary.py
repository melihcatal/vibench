import os
import anthropic
from typing import List, Dict, Any


def moderation_summary(results: List[Dict[str, Any]]) -> str:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = (
        "Provide a concise summary report of these text moderation results, including stats on flagged items and common violation categories:\\n"
        + str(results)
    )
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
