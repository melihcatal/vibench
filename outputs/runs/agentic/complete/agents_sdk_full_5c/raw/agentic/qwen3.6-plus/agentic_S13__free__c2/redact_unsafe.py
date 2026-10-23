"""
redact_unsafe.py - Flags or redacts unsafe spans from text.

Uses the OpenAI Moderation API (api.openai.com) with the text-moderation-latest model
to identify unsafe content and redact flagged portions from user text.
"""

import os
import re
import openai


SAFETY_CATEGORIES = [
    "hate",
    "hate/threatening",
    "harassment",
    "harassment/threatening",
    "self-harm",
    "self-harm/intent",
    "self-harm/instructions",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
]

REDACTION_THRESHOLD = 0.5
REDACTION_MARKER = "[REDACTED]"


def _get_moderation_client():
    """Create an OpenAI moderation client using the official SDK."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = openai.OpenAI(api_key=api_key)
    return client


def redact_unsafe(
    text: str,
    threshold: float = REDACTION_THRESHOLD,
    marker: str = REDACTION_MARKER,
    categories: list = None,
) -> dict:
    """
    Flag and redact unsafe spans from text using OpenAI Moderation API.

    The text is split into sentences, each sentence is moderated, and unsafe
    sentences are replaced with the redaction marker.

    Args:
        text: The user text to process.
        threshold: Minimum score to flag a category as violated.
        marker: Replacement string for redacted content.
        categories: Optional list of categories to check. If None, all are checked.

    Returns:
        Dictionary with:
            - original_text: the input text
            - redacted_text: text with unsafe spans replaced
            - flagged_spans: list of dicts with span text and reasons
            - provider: openai
    """
    client = _get_moderation_client()

    sentences = re.split(r'(?<=[.!?])\s+', text)
    flagged_spans = []
    redacted_sentences = []

    for sentence in sentences:
        if not sentence.strip():
            redacted_sentences.append(sentence)
            continue

        result = client.moderations.create(
            input=sentence,
            model="text-moderation-latest",
        )

        moderation = result.results[0]
        is_unsafe = moderation.flagged
        violating_cats = []

        for category in (categories or SAFETY_CATEGORIES):
            score = getattr(moderation.category_scores, category, 0.0)
            if score >= threshold:
                violating_cats.append(category)

        if is_unsafe and violating_cats:
            flagged_spans.append({
                "span_text": sentence,
                "categories": violating_cats,
            })
            redacted_sentences.append(marker)
        else:
            redacted_sentences.append(sentence)

    redacted_text = " ".join(redacted_sentences)

    return {
        "original_text": text,
        "redacted_text": redacted_text,
        "flagged_spans": flagged_spans,
        "redaction_count": len(flagged_spans),
        "model": "text-moderation-latest",
        "provider": "openai",
        "provider_endpoint": "api.openai.com/v1/moderations",
    }


def flag_unsafe_spans(text: str, threshold: float = REDACTION_THRESHOLD) -> list[dict]:
    """
    Identify and return unsafe spans without redacting them.

    Args:
        text: The user text to analyze.
        threshold: Minimum score to flag a category.

    Returns:
        List of flagged spans with their text and violating categories.
    """
    result = redact_unsafe(text, threshold=threshold)
    return result["flagged_spans"]


def get_redaction_summary(text: str, threshold: float = REDACTION_THRESHOLD) -> dict:
    """
    Get a summary of redaction operations for the given text.

    Args:
        text: The user text to analyze.
        threshold: Minimum score to flag a category.

    Returns:
        Summary dict with redaction statistics.
    """
    result = redact_unsafe(text, threshold=threshold)
    total_spans = len(re.split(r'(?<=[.!?])\s+', text))

    category_breakdown = {}
    for span in result["flagged_spans"]:
        for cat in span["categories"]:
            category_breakdown[cat] = category_breakdown.get(cat, 0) + 1

    return {
        "total_spans_analyzed": total_spans,
        "redacted_count": result["redaction_count"],
        "category_breakdown": category_breakdown,
        "redaction_ratio": result["redaction_count"] / total_spans if total_spans > 0 else 0.0,
        "provider": "openai",
    }


if __name__ == "__main__":
    import sys
    sample_text = sys.argv[1] if len(sys.argv) > 1 else "This is a test message with potentially unsafe content."
    result = redact_unsafe(sample_text)
    print(f"Redacted: {result['redacted_text']}")
    print(f"Flagged spans: {result['redaction_count']}")
