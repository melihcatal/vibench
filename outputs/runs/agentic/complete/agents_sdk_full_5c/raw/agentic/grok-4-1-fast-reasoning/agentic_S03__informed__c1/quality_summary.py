import os
from anthropic import Anthropic

def quality_summary(original: str, translated: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY required")
    client = Anthropic(api_key=api_key)
    prompt = f"""Analyze the translation quality and summarize any issues such as inaccuracies, unnatural phrasing, or omissions.

Original text: {original}

Translated text: {translated}

Provide a concise summary of issues, or "No significant issues detected" if the translation is high quality."""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text