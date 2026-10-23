import os
import anthropic
from typing import List
from security_models import CryptoEvent


def summarize_key_usage(events: List[CryptoEvent]) -> str:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f"""Summarize key usage and crypto events:\\n{events}"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
