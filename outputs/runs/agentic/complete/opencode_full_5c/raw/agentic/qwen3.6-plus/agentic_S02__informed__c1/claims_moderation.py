import os
import requests
from typing import List, Optional

from identity_models import ModerationResult


PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY", "")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_claims_text(
    text: str,
    languages: Optional[List[str]] = None,
    requested_attributes: Optional[List[str]] = None,
    threshold: float = 0.7,
) -> ModerationResult:
    if languages is None:
        languages = ["en"]
    if requested_attributes is None:
        requested_attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
            "SEXUALLY_EXPLICIT",
            "FLIRTATION",
        ]

    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in requested_attributes},
        "languages": languages,
        "doNotStore": True,
    }

    params = {"key": PERSPECTIVE_API_KEY}

    response = requests.post(
        PERSPECTIVE_API_URL,
        json=payload,
        params=params,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    attribute_scores = {}
    flagged_attributes = []
    max_score = 0.0

    attribute_scores_data = data.get("attributeScores", {})
    for attr_name, attr_data in attribute_scores_data.items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        attribute_scores[attr_name] = score
        if score > max_score:
            max_score = score
        if score >= threshold:
            flagged_attributes.append(attr_name)

    is_safe = max_score < threshold

    return ModerationResult(
        text=text,
        is_safe=is_safe,
        toxicity_score=max_score,
        categories=attribute_scores,
        flagged_attributes=flagged_attributes,
        provider="perspective_api",
    )


def moderate_multiple_claims(
    texts: List[str],
    languages: Optional[List[str]] = None,
    threshold: float = 0.7,
) -> List[ModerationResult]:
    results = []
    for text in texts:
        result = moderate_claims_text(
            text=text,
            languages=languages,
            threshold=threshold,
        )
        results.append(result)
    return results


def get_moderation_summary(
    results: List[ModerationResult],
) -> dict:
    total = len(results)
    flagged = sum(1 for r in results if not r.is_safe)
    safe = total - flagged

    avg_toxicity = 0.0
    if total > 0:
        avg_toxicity = sum(r.toxicity_score for r in results) / total

    all_categories = set()
    for r in results:
        all_categories.update(r.categories.keys())

    category_averages = {}
    for cat in all_categories:
        scores = [r.categories.get(cat, 0.0) for r in results]
        category_averages[cat] = sum(scores) / len(scores) if scores else 0.0

    return {
        "total_moderated": total,
        "safe_count": safe,
        "flagged_count": flagged,
        "flagged_percentage": (flagged / total * 100) if total > 0 else 0,
        "average_toxicity_score": avg_toxicity,
        "category_averages": category_averages,
        "provider": "perspective_api",
    }
