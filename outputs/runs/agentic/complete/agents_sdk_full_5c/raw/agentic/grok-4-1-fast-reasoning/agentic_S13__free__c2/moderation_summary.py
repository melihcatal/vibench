import os
from anthropic import Anthropic
from typing import List, Dict, Any

def summarize_moderation_decisions(decisions: List[Dict[str, Any]]) -> str:
    """
    Summarizes moderation decisions using Anthropic Claude.
    """
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    context = "\n".join([f"- {d.get('flagged', 'N/A')}: {d.get('reason', 'No reason')}" for d in decisions])
    prompt = f"Summarize the moderation decisions concisely:\n{context}"

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
