"""
Summarize moderation decisions using Anthropic Messages API.
"""
import os
from typing import List
import anthropic
from anthropic.types import Message


def summarize_moderation(decisions: List[dict]) -> str:
    """Summarize moderation decisions using Anthropic Claude."""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    decision_texts = []
    for decision in decisions:
        decision_texts.append(
            f"Text: {decision['text']}\n"
            f"Flagged: {decision['flagged']}\n"
            f"Details: {decision['decisions']}"
        )
    
    prompt = (
        "Summarize the following moderation decisions in a concise report. "
        "Include overall flagged rate and key categories.\n\n"
        f"{'\\n\\n'.join(decision_texts)}"
    )
    
    message: Message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text