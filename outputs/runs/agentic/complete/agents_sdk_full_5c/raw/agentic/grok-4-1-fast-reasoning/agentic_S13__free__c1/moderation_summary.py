from typing import List, Any
from safety_client import anthropic_client

def moderation_summary(decisions: List[Dict[str, Any]]) -> str:
    client = anthropic_client()
    prompt = "Summarize the moderation decisions across these cases. Highlight common violations, total flagged, and patterns:\\n" + str(decisions)
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text