import os
from typing import List, Dict, Any
from anthropic import Anthropic


def moderation_summary(decisions: List[Dict[str, Any]]) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("Anthropic API key not configured")

    client = Anthropic(api_key=api_key)

    blocked_count = sum(1 for d in decisions if d.get("overall_decision") == "BLOCK")
    total_count = len(decisions)

    summary_prompt = f"""You are a content moderation analyst. Summarize the following moderation decisions:

Total messages: {total_count}
Blocked messages: {blocked_count}
Allowed messages: {total_count - blocked_count}

Recent decisions (last 5):
{chr(10).join([f"- {d.get('text', '')[:50]}...: {d.get('overall_decision', 'UNKNOWN')}" for d in decisions[:5]])}

Provide a concise summary of the moderation activity, highlighting any patterns or concerning trends."""

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=300,
        messages=[{"role": "user", "content": summary_prompt}],
    )

    return response.content[0].text
