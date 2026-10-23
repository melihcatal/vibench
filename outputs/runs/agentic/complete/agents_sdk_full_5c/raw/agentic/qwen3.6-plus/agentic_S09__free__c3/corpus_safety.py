"""
Check corpus text before embedding.

Provider: OpenAI Moderation API
Provider SDK: openai
Provider Model: text-embedding-3-small / omni-moderation-latest
Provider Env: OPENAI_API_KEY
Provider Host: api.openai.com
"""

from dataclasses import dataclass, field
from typing import Any

from openai import OpenAI


@dataclass
class SafetyResult:
    """Result of a safety check on a text item."""
    text: str
    is_safe: bool
    flagged_categories: list[str] = field(default_factory=list)
    scores: dict[str, float] = field(default_factory=dict)


def check_corpus_safety(
    texts: list[str],
    moderation_model: str = "omni-moderation-latest",
    flagged_threshold: float = 0.5,
) -> list[SafetyResult]:
    """Check a corpus of texts for safety issues using OpenAI Moderation API.

    Args:
        texts: List of text strings to check before embedding.
        moderation_model: OpenAI moderation model (default: omni-moderation-latest).
        flagged_threshold: Score threshold above which a category is flagged.

    Returns:
        List of SafetyResult objects, one per input text.
    """
    client = OpenAI()
    results: list[SafetyResult] = []

    for text in texts:
        response = client.moderations.create(
            model=moderation_model,
            input=text,
        )
        result_obj = response.results[0]
        flagged_cats = []
        category_scores = {}

        for cat_name, flagged in result_obj.flagged_categories:
            if flagged:
                flagged_cats.append(cat_name)

        # Extract category scores
        if hasattr(result_obj, "category_scores"):
            for cat_name, score in result_obj.category_scores.items():
                category_scores[cat_name] = round(score, 6)

        results.append(SafetyResult(
            text=text,
            is_safe=not result_obj.flagged,
            flagged_categories=flagged_cats,
            scores=category_scores,
        ))

    return results


def filter_safe_texts(
    texts: list[str],
    moderation_model: str = "omni-moderation-latest",
) -> list[str]:
    """Return only texts that pass safety checks via OpenAI moderation.

    Args:
        texts: List of text strings to filter.
        moderation_model: OpenAI moderation model to use.

    Returns:
        List of texts that passed moderation (not flagged).
    """
    safety_results = check_corpus_safety(texts, moderation_model=moderation_model)
    return [r.text for r in safety_results if r.is_safe]


if __name__ == "__main__":
    sample_texts = [
        "The sun sets over the calm ocean waters.",
        "I love spending time with my family at the park.",
        "This is a completely benign and safe sentence.",
    ]
    results = check_corpus_safety(sample_texts)
    for r in results:
        print(f"Safe: {r.is_safe} | Text: {r.text[:50]}...")
