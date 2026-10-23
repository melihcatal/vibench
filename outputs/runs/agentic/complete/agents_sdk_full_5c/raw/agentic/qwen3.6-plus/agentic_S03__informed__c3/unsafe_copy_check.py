"""Check localized copy for unsafe content using the Anthropic Messages API.

Provider: Anthropic Messages API (anthropic SDK)
Model: claude-3-5-sonnet-latest
Auth: ANTHROPIC_API_KEY
"""

from __future__ import annotations

import json
import os
from typing import Optional

import anthropic


SAFETY_SYSTEM_PROMPT = """You are a content safety reviewer for localized marketing copy.
Review the provided text and flag any unsafe or problematic content.

Check for:
- hate_speech: discriminatory or hateful language
- self_harm: references to self-harm or suicide
- sexual_content: sexually explicit or inappropriate content
- violence: graphic violence or threats
- personal_info: leaked PII or sensitive personal data
- profanity: vulgar or offensive language
- brand_safety: content that could harm brand reputation
- cultural_sensitivity: culturally inappropriate content in the target locale

Return a JSON object with:
- safe: boolean indicating overall safety
- flags: list of {category, severity (low/medium/high/critical), description}
- recommendation: "approve", "review", or "reject"
"""


def check_unsafe_copy(
    text: str,
    locale: str = "",
    model: str = "claude-3-5-sonnet-latest",
    api_key: Optional[str] = None,
) -> dict:
    """Check translated/localized copy for unsafe content via Anthropic API.

    Args:
        text: The localized copy to review.
        locale: Target locale for cultural context (e.g. 'ja-JP', 'de-DE').
        model: Anthropic model identifier (default: claude-3-5-sonnet-latest).
        api_key: Anthropic API key; falls back to ANTHROPIC_API_KEY env var.

    Returns:
        Dict with safe flag, issues list, and recommendation.
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=key)

    locale_context = f"Target locale: {locale}" if locale else ""
    user_prompt = (
        f"Review the following localized copy for unsafe content.\n"
        f"{locale_context}\n\n"
        f"Copy to review:\n{text}\n\n"
        f"Return a JSON safety analysis."
    )

    message = client.messages.create(
        model=model,
        system=SAFETY_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
        max_tokens=1024,
        temperature=0.0,
    )

    content = ""
    for block in message.content:
        if block.type == "text":
            content += block.text

    content = content.strip()

    try:
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        return json.loads(content)
    except (json.JSONDecodeError, IndexError):
        return {
            "safe": True,
            "flags": [],
            "recommendation": "review",
            "note": "Failed to parse LLM response; manual review advised.",
        }


def check_unsafe_copy_batch(
    texts: list[str],
    locale: str = "",
) -> list[dict]:
    """Check multiple pieces of localized copy sequentially."""
    results = []
    for text in texts:
        analysis = check_unsafe_copy(text, locale=locale)
        results.append(analysis)
    return results
