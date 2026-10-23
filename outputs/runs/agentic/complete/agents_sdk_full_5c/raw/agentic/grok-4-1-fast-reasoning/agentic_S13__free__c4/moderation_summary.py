import anthropic
from typing import List, Any
from safety_client import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def moderation_summary(decisions: List[dict]) -> str:
    prompt = f"""Provide a concise summary of these moderation decisions:
{decisions}"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text