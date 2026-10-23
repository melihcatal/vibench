"""Summarize translation quality issues using a hosted LLM.

Provider: Mistral Chat API (mistralai SDK)
Model: mistral-large-latest
Auth: MISTRAL_API_KEY
"""

from __future__ import annotations

import json
import os
from typing import Optional

import mistralai


SYSTEM_PROMPT = """You are a translation quality analyst. Review the source text and its translation, then identify any quality issues.

Possible issue categories:
- accuracy: mistranslation or wrong meaning
- fluency: unnatural phrasing or grammar errors
- tone: inappropriate register or formality
- terminology: inconsistent or wrong domain terms
- completeness: missing content or untranslated segments
- formatting: broken markup or layout issues

Return a JSON object with:
- score: 0.0 to 1.0 overall quality score
- issues: list of {category, severity (low/medium/high), description}
- summary: brief one-line summary of quality assessment
"""


def summarize_translation_quality(
    source_text: str,
    translated_text: str,
    source_lang: str = "",
    target_lang: str = "EN",
    model: str = "mistral-large-latest",
    api_key: Optional[str] = None,
) -> dict:
    """Analyze translation quality via Mistral Chat API.

    Args:
        source_text: Original source text.
        translated_text: Machine or human translation.
        source_lang: Source language for context.
        target_lang: Target language for context.
        model: Mistral model identifier (default: mistral-large-latest).
        api_key: Mistral API key; falls back to MISTRAL_API_KEY env var.

    Returns:
        Dict with score, issues list, and summary.
    """
    key = api_key or os.environ.get("MISTRAL_API_KEY", "")
    if not key:
        raise ValueError("MISTRAL_API_KEY environment variable is required")

    client = mistralai.Mistral(api_key=key)

    user_prompt = (
        f"Source ({source_lang}): {source_text}\n"
        f"Translation ({target_lang}): {translated_text}\n"
        f"\nReview the quality of this translation and return a JSON analysis."
    )

    response = client.chat.complete(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
    )

    content = response.choices[0].message.content.strip() if response.choices else ""

    # Try to parse JSON from the response
    try:
        # Handle potential markdown code block wrapping
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        return json.loads(content)
    except (json.JSONDecodeError, IndexError):
        return {
            "score": 0.5,
            "issues": [{"category": "parse_error", "severity": "medium",
                         "description": "Failed to parse LLM response as JSON"}],
            "summary": content[:200] if content else "No analysis available",
        }


def batch_summarize_quality(
    pairs: list[tuple[str, str]],
    source_lang: str = "",
    target_lang: str = "EN",
) -> list[dict]:
    """Analyze multiple translation pairs sequentially via Mistral."""
    results = []
    for source, translated in pairs:
        analysis = summarize_translation_quality(
            source, translated, source_lang, target_lang
        )
        results.append(analysis)
    return results
