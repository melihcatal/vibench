"""Summarize translation quality issues using Anthropic Claude API.

Analyzes source/target text pairs and generates a quality summary
report identifying potential issues like mistranslation, tone mismatch,
missing content, or formatting problems.
"""

import json
import os
from typing import Any

import anthropic

QUALITY_PROMPT = """You are a professional translation quality analyst. Analyze the following source text and its translation for quality issues.

Source ({source_lang}):
{source_text}

Translation ({target_lang}):
{target_text}

Evaluate the translation across these dimensions:
1. Accuracy: Does the translation faithfully convey the original meaning?
2. Fluency: Is the translation natural and grammatically correct in the target language?
3. Tone/Register: Does the translation match the tone and formality of the original?
4. Completeness: Is any content missing or added without justification?
5. Terminology: Are domain-specific terms handled correctly?

Respond with a JSON object containing:
- "overall_score": 1-10 integer score
- "issues": array of objects with "category", "severity" (low/medium/high), "description", and "suggestion"
- "summary": brief overall assessment (2-3 sentences)
- "safe_for_publication": boolean
"""


def summarize_translation_quality(
    source_text: str,
    target_text: str,
    source_lang: str,
    target_lang: str,
    model: str = "claude-3-5-sonnet-20241022",
) -> dict[str, Any]:
    """Analyze translation quality and return a structured summary using Anthropic Claude.

    Args:
        source_text: Original source text.
        target_text: Translated text to evaluate.
        source_lang: Source language code.
        target_lang: Target language code.
        model: Anthropic Claude model identifier.

    Returns:
        Dictionary with overall_score, issues, summary, and safe_for_publication.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required for Anthropic API access")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = QUALITY_PROMPT.format(
        source_lang=source_lang,
        target_lang=target_lang,
        source_text=source_text,
        target_text=target_text,
    )

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=0.0,
        system="You are a translation quality analyst. Always respond with valid JSON.",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    response_text = ""
    for block in message.content:
        if hasattr(block, "text"):
            response_text += block.text

    # Extract JSON from response (handle possible markdown wrapper)
    response_text = response_text.strip()
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.startswith("```"):
        response_text = response_text[3:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]
    response_text = response_text.strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {
            "overall_score": 0,
            "issues": [{"category": "parsing_error", "severity": "high", "description": "Failed to parse quality analysis response", "suggestion": "Review the translation manually"}],
            "summary": "Analysis response could not be parsed.",
            "safe_for_publication": False,
        }


def batch_quality_summary(
    pairs: list[dict[str, str]],
    model: str = "claude-3-5-sonnet-20241022",
) -> list[dict[str, Any]]:
    """Evaluate quality for multiple source/target text pairs using Anthropic Claude.

    Args:
        pairs: List of dicts with keys 'source_text', 'target_text', 'source_lang', 'target_lang'.
        model: Anthropic Claude model identifier.

    Returns:
        List of quality summary dictionaries corresponding to each input pair.
    """
    results: list[dict[str, Any]] = []
    for pair in pairs:
        result = summarize_translation_quality(
            source_text=pair["source_text"],
            target_text=pair["target_text"],
            source_lang=pair["source_lang"],
            target_lang=pair["target_lang"],
            model=model,
        )
        results.append(result)
    return results
