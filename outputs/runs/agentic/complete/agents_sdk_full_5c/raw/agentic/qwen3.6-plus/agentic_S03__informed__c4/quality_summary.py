"""
Summarize translation quality issues using hosted LLM inference.

Provider: Anthropic Messages API
SDK: anthropic
Auth: ANTHROPIC_API_KEY

Uses Claude to analyze translated text pairs and generate a structured
quality summary identifying issues like mistranslation, omission,
fluency problems, and tone mismatch.

Model: claude-3-haiku-20240307 for fast quality analysis, or
claude-3-5-sonnet-20241022 for more thorough analysis.
"""

import json
import os
from typing import Optional

import anthropic

from translation_models import TranslationResult


# Concrete Anthropic model identifiers
QUALITY_MODEL_FAST = "claude-3-haiku-20240307"
QUALITY_MODEL_DETAILED = "claude-3-5-sonnet-20241022"


def get_anthropic_client() -> anthropic.Anthropic:
    """Create an Anthropic client using the API key from environment."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is required. "
            "Set it with your Anthropic API key."
        )
    return anthropic.Anthropic(api_key=api_key)


def summarize_translation_quality(
    source_text: str,
    translated_text: str,
    source_lang: str,
    target_lang: str,
    *,
    model: str = QUALITY_MODEL_FAST,
    client: Optional[anthropic.Anthropic] = None,
) -> dict:
    """
    Analyze a source/translation pair and return a quality summary.

    Uses Anthropic Claude to identify:
    - Accuracy issues (mistranslations, additions, omissions)
    - Fluency and naturalness in the target language
    - Tone and register matching
    - Formatting and structural preservation
    - Overall quality score (1-5)

    Args:
        source_text: Original source text.
        translated_text: Translated text to evaluate.
        source_lang: Source language code.
        target_lang: Target language code.
        model: Anthropic model ID. Defaults to claude-3-haiku-20240307.
            Use claude-3-5-sonnet-20241022 for deeper analysis.
        client: Optional pre-created Anthropic client.

    Returns:
        Dict with quality analysis results including score, issues,
        and recommendations.
    """
    if client is None:
        client = get_anthropic_client()

    system_prompt = (
        "You are a professional translation quality evaluator. "
        "Analyze the provided source text and its translation, then "
        "return ONLY a valid JSON object with the following structure:\n"
        "{\n"
        '  "overall_score": <integer 1-5>,\n'
        '  "accuracy_score": <integer 1-5>,\n'
        '  "fluency_score": <integer 1-5>,\n'
        '  "tone_match_score": <integer 1-5>,\n'
        '  "issues": [\n'
        '    {"type": "<mistranslation|omission|addition|fluency|tone|formatting>",\n'
        '     "description": "<brief description>",\n'
        '     "severity": "<critical|major|minor>",\n'
        '     "source_segment": "<relevant source text>",\n'
        '     "translated_segment": "<relevant translation>"}\n'
        "  ],\n"
        '  "summary": "<one-sentence overall assessment>",\n'
        '  "recommendations": ["<actionable recommendation 1>", "..."]\n'
        "}\n"
        "Do not include any text outside the JSON object."
    )

    user_prompt = (
        f"Source language: {source_lang}\n"
        f"Target language: {target_lang}\n\n"
        f"Source text:\n{source_text}\n\n"
        f"Translated text:\n{translated_text}\n\n"
        "Provide your quality assessment as JSON."
    )

    message = client.messages.create(
        model=model,
        max_tokens=2048,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt},
        ],
    )

    response_text = message.content[0].text.strip()

    # Parse JSON from the response, handling potential markdown wrapping
    if response_text.startswith("```"):
        # Remove markdown code fences if present
        lines = response_text.split("\n")
        json_lines = [
            line for line in lines
            if not line.strip().startswith("```")
        ]
        response_text = "\n".join(json_lines)

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {
            "overall_score": 0,
            "accuracy_score": 0,
            "fluency_score": 0,
            "tone_match_score": 0,
            "issues": [
                {
                    "type": "parsing_error",
                    "description": "Failed to parse quality analysis response",
                    "severity": "major",
                    "source_segment": "",
                    "translated_segment": "",
                }
            ],
            "summary": "Quality analysis response could not be parsed.",
            "recommendations": ["Retry the analysis."],
        }


def batch_quality_summary(
    translation_pairs: list[tuple[str, str]],
    source_lang: str,
    target_lang: str,
    *,
    model: str = QUALITY_MODEL_FAST,
    client: Optional[anthropic.Anthropic] = None,
) -> list[dict]:
    """
    Analyze multiple translation pairs and return quality summaries.

    Args:
        translation_pairs: List of (source, translated) tuples.
        source_lang: Source language code.
        target_lang: Target language code.
        model: Anthropic model ID.
        client: Optional pre-created Anthropic client.

    Returns:
        List of quality summary dicts, one per translation pair.
    """
    results = []
    for source, translated in translation_pairs:
        summary = summarize_translation_quality(
            source_text=source,
            translated_text=translated,
            source_lang=source_lang,
            target_lang=target_lang,
            model=model,
            client=client,
        )
        results.append(summary)
    return results


if __name__ == "__main__":
    result = summarize_translation_quality(
        source_text="The quick brown fox jumps over the lazy dog.",
        translated_text="El rápido zorro marrón salta sobre el perro perezoso.",
        source_lang="EN",
        target_lang="ES",
    )
    print(json.dumps(result, indent=2))
