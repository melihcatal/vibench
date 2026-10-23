import anthropic
import json
from typing import List, Dict, Any
from safety_client import get_api_key


def moderation_summary(decisions: List[Dict[str, Any]]) -> str:
    api_key = get_api_key("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)
    decisions_json = json.dumps(decisions, indent=2)
    prompt = f"""Provide a concise summary of these moderation decisions, including count of flagged items, common categories, and overall trends:

{decisions_json}"""
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=400,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
