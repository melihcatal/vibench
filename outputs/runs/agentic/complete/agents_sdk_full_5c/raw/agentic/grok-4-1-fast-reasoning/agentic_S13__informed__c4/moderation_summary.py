from anthropic import Anthropic
import os

def summarize_moderation_decisions(decisions: list[dict]) -> str:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    decisions_str = "\n".join([
        f"Text: {d.get('input_text', d.get('text', ''))[:100]}... Flagged: {d.get('flagged', False)} Categories/Scores: {d.get('categories', d.get('scores', {}))}"
        for d in decisions
    ])
    prompt = f"""Summarize the moderation decisions below. Include count of flagged items, top categories, and key patterns.

Decisions:
{decisions_str}

Summary:"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text