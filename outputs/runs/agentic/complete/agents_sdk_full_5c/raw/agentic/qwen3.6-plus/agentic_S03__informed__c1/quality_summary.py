"""
Summarize translation quality issues using a hosted LLM.

Provider: Anthropic Messages API
SDK: anthropic
Auth: ANTHROPIC_API_KEY
Model: claude-3-5-sonnet-20241022
"""

import os
from typing import Any, Dict, List, Optional

import anthropic

from translate_text import translate_text


def summarize_translation_quality(
    original_texts: List[str],
    translated_texts: List[str],
    source_lang: str,
    target_lang: str,
    custom_criteria: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Summarize translation quality issues between original and translated texts.

    Uses Anthropic Claude (claude-3-5-sonnet-20241022) to analyze translation
    pairs and produce a structured quality summary.

    Args:
        original_texts: List of original source texts.
        translated_texts: List of translated texts (parallel to originals).
        source_lang: Source language code.
        target_lang: Target language code.
        custom_criteria: Optional list of specific quality criteria to evaluate.

    Returns:
        Dictionary containing quality summary with issues found and recommendations.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required.")

    client = anthropic.Anthropic(api_key=api_key)

    criteria = custom_criteria or [
        "Accuracy of meaning",
        "Tone and formality consistency",
        "Cultural appropriateness",
        "Grammar and syntax in target language",
    ]

    # Build a summary of text pairs for analysis
    pair_summaries = []
    for i, (orig, trans) in enumerate(zip(original_texts, translated_texts), 1):
        pair_summaries.append(
            f"Pair {i}:\n"
            f"  [{source_lang}] {orig}\n"
            f"  [{target_lang}] {trans}\n"
        )

    prompt = (
        f"Analyze the following translation pairs from {source_lang} to {target_lang} "
        f"and provide a quality summary.\n\n"
        f"Evaluate against these criteria: {', '.join(criteria)}\n\n"
        f"--- Translation Pairs ---\n"
        f"{''.join(pair_summaries)}\n"
        f"--- End Pairs ---\n\n"
        f"Provide your analysis in the following JSON-like structure:\n"
        f"- Overall quality score (1-10)\n"
        f"- Per-criterion assessment\n"
        f"- Specific issues found (quote the problematic translations)\n"
        f"- Recommendations for improvement\n"
        f"- Whether any translations should be flagged for human review"
    )

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        temperature=0.3,
        system=(
            "You are a professional translation quality analyst. "
            "Analyze translation pairs and provide structured, actionable feedback. "
            "Be specific about issues and reference the exact text when describing problems."
        ),
        messages=[{"role": "user", "content": prompt}],
    )

    analysis_text = ""
    for block in message.content:
        if hasattr(block, "text"):
            analysis_text += block.text

    return {
        "source_lang": source_lang,
        "target_lang": target_lang,
        "total_pairs_analyzed": len(original_texts),
        "model": "claude-3-5-sonnet-20241022",
        "analysis": analysis_text,
        "criteria_evaluated": criteria,
    }


def check_single_translation_quality(
    original: str,
    translated: str,
    source_lang: str,
    target_lang: str,
) -> Dict[str, Any]:
    """
    Check the quality of a single translation pair.

    Args:
        original: Original source text.
        translated: Translated text.
        source_lang: Source language code.
        target_lang: Target language code.

    Returns:
        Quality assessment dictionary.
    """
    return summarize_translation_quality(
        original_texts=[original],
        translated_texts=[translated],
        source_lang=source_lang,
        target_lang=target_lang,
    )


if __name__ == "__main__":
    originals = ["The quick brown fox jumps over the lazy dog.", "Hello, how are you?"]
    translations = [
        "Der schnelle braune Fuchs springt über den faulen Hund.",
        "Hallo, wie geht es Ihnen?",
    ]
    summary = summarize_translation_quality(
        originals, translations, "EN", "DE"
    )
    print(summary["analysis"])
