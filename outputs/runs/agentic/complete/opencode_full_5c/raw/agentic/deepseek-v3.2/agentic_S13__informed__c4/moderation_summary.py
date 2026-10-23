import os
from typing import List, Dict
import anthropic


def moderation_summary(decisions: List[Dict]) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("Anthropic API key not configured")

    client = anthropic.Anthropic(api_key=api_key)

    summary_prompt = f"""Summarize the following moderation decisions:

{decisions}

Provide a concise summary including:
1. Total number of items moderated
2. Number of allowed vs blocked items
3. Main categories of violations
4. Any patterns or trends observed

Keep the summary brief and actionable for moderation reviewers."""

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=500,
        temperature=0.3,
        messages=[{"role": "user", "content": summary_prompt}],
    )

    return response.content[0].text
