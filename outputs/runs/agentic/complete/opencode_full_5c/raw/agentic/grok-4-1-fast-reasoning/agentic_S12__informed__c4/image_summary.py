import os
import json
from anthropic import Anthropic


def image_summary(analysis: dict) -> str:
    """
    Summarize visual analysis results using Anthropic Claude.
    analysis keys: 'labels', 'description', 'texts', 'safety'
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Set ANTHROPIC_API_KEY")

    client = Anthropic(api_key=api_key)

    labels_str = json.dumps(analysis.get("labels", []))
    desc = analysis.get("description", {}).get("description", "No description")
    texts_str = json.dumps(analysis.get("texts", []))
    safety_str = json.dumps(analysis.get("safety", {}))

    prompt = f"""Provide a short summary of the image visual analysis:

Labels: {labels_str}
Description: {desc}
Text: {texts_str}
Safety: {safety_str}

Summary (1-2 sentences):"""

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=120,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
