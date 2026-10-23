import os
from typing import List
from anthropic import Anthropic
from safety_models import ModerationDecision

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def moderation_summary(decisions: List[ModerationDecision]) -> str:
    prompt = f"""Provide a concise summary of these moderation decisions:
- Total cases: {len(decisions)}
- Blocked cases: {sum(1 for d in decisions if d["decision"] == "block")}
- Common violations: analyze patterns in scores and categories.

Details: {decisions}"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
