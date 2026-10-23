"""
moderate_batch.py - Moderates a batch of user messages and returns per-message decisions.

Uses the OpenAI Moderation API (api.openai.com) with the text-moderation-latest model
to process multiple messages in a single batch request.
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

BATCH_SEVERITY_THRESHOLD = 0.5


def _get_moderation_client():
    """Create an OpenAI moderation client using the official SDK."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = openai.OpenAI(api_key=api_key)
    return client


def moderate_batch(
    messages: list[str],
    severity_threshold: float = BATCH_SEVERITY_THRESHOLD,
) -> list[dict]:
    """
    Moderate a batch of user messages and return per-message decisions.

    Args:
        messages: List of user messages to moderate.
        severity_threshold: Minimum score to flag a category as violated.

    Returns:
        List of dicts, one per message, with moderation results:
            - message_index: index in the original list
            - flagged: bool
            - category_scores: dict of category -> score
            - flagged_categories: list of categories exceeding threshold
            - model: the moderation model used
    """
    client = _get_moderation_client()

    result = client.moderations.create(
        input=messages,
        model="text-moderation-latest",
    )

    batch_results = []
    for idx, moderation_result in enumerate(result.results):
        category_scores = {}
        flagged_categories = []

        for category in SAFETY_CATEGORIES:
            score = getattr(moderation_result.category_scores, category, 0.0)
            category_scores[category] = score
            if score >= severity_threshold:
                flagged_categories.append(category)

        batch_results.append({
            "message_index": idx,
            "flagged": moderation_result.flagged,
            "category_scores": category_scores,
            "flagged_categories": flagged_categories,
            "model": "text-moderation-latest",
            "provider": "openai",
            "provider_endpoint": "api.openai.com/v1/moderations",
        })

    return batch_results


def moderate_batch_with_filter(
    messages: list[str],
    severity_threshold: float = BATCH_SEVERITY_THRESHOLD,
    categories: list = None,
) -> list[dict]:
    """
    Moderate a batch and return only results for messages that failed moderation.

    Args:
        messages: List of user messages to moderate.
        severity_threshold: Minimum score to flag a category.
        categories: Optional list of categories to focus on.

    Returns:
        List of moderation results only for flagged messages.
    """
    results = moderate_batch(messages, severity_threshold)
    flagged_results = [r for r in results if r["flagged"]]

    if categories:
        for r in flagged_results:
            r["category_scores"] = {
                k: v for k, v in r["category_scores"].items() if k in categories
            }
            r["flagged_categories"] = [
                c for c in r["flagged_categories"] if c in categories
            ]

    return flagged_results


def get_batch_summary(batch_results: list[dict]) -> dict:
    """
    Generate a summary of batch moderation results.

    Args:
        batch_results: Output from moderate_batch().

    Returns:
        Summary dict with total messages, flagged count, and category breakdown.
    """
    total = len(batch_results)
    flagged_count = sum(1 for r in batch_results if r["flagged"])

    category_counts = {}
    for result in batch_results:
        for cat in result.get("flagged_categories", []):
            category_counts[cat] = category_counts.get(cat, 0) + 1

    return {
        "total_messages": total,
        "flagged_count": flagged_count,
        "safe_count": total - flagged_count,
        "flag_rate": flagged_count / total if total > 0 else 0.0,
        "category_counts": category_counts,
        "provider": "openai",
    }


if __name__ == "__main__":
    sample_messages = [
        "Hello, how are you today?",
        "This is inappropriate content with threats.",
        "Just a normal message about the weather.",
    ]
    results = moderate_batch(sample_messages)
    for r in results:
        status = "FLAGGED" if r["flagged"] else "SAFE"
        print(f"[{status}] Message {r['message_index']}: {r['flagged_categories']}")
