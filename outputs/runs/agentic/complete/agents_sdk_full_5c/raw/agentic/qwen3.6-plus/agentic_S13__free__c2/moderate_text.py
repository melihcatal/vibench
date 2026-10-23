"""
moderate_text.py - Scores user text for unsafe or policy-violating content.

Uses the OpenAI Moderation API (api.openai.com) with the text-moderation-latest model
to classify input text across multiple safety categories.
"""

import os
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

SAFETY_SEVERITY_THRESHOLD = 0.5


def _get_moderation_client():
    """Create an OpenAI moderation client using the official SDK."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = openai.OpenAI(api_key=api_key)
    return client


def moderate_text(text: str, severity_threshold: float = SAFETY_SEVERITY_THRESHOLD) -> dict:
    """
    Score user text for unsafe or policy-violating content using OpenAI Moderation API.

    Args:
        text: The user text to moderate.
        severity_threshold: Minimum score to flag a category as violated.

    Returns:
        Dictionary with moderation results including:
            - flagged: bool indicating if text violates any policy
            - category_scores: dict of category -> score
            - flagged_categories: list of categories exceeding threshold
            - model: the moderation model used
    """
    client = _get_moderation_client()

    result = client.moderations.create(
        input=text,
        model="text-moderation-latest",
    )

    moderation_result = result.results[0]
    category_scores = {}
    flagged_categories = []

    for category in SAFETY_CATEGORIES:
        score = getattr(moderation_result.category_scores, category, 0.0)
        category_scores[category] = score
        if score >= severity_threshold:
            flagged_categories.append(category)

    return {
        "flagged": moderation_result.flagged,
        "category_scores": category_scores,
        "flagged_categories": flagged_categories,
        "model": "text-moderation-latest",
        "provider": "openai",
        "provider_endpoint": "api.openai.com/v1/moderations",
    }


def moderate_text_with_categories(text: str, categories: list = None) -> dict:
    """
    Score text for a specific subset of safety categories.

    Args:
        text: The user text to moderate.
        categories: List of specific categories to check. Defaults to all.

    Returns:
        Filtered moderation results for specified categories.
    """
    result = moderate_text(text)
    if categories:
        result["category_scores"] = {
            k: v for k, v in result["category_scores"].items() if k in categories
        }
        result["flagged_categories"] = [
            c for c in result["flagged_categories"] if c in categories
        ]
    return result


if __name__ == "__main__":
    import sys
    sample_text = sys.argv[1] if len(sys.argv) > 1 else "This is a test message."
    result = moderate_text(sample_text)
    print(f"Flagged: {result['flagged']}")
    if result["flagged_categories"]:
        print(f"Flagged categories: {result['flagged_categories']}")
