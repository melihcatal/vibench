import os
from typing import List, Dict
from safety_models import ModerationRequest, moderate_text
from safety_client import get_client

# SAME-SCENARIO
# Moderates a batch of user messages and returns per-message decisions.
# Provider identification: PERSPECTIVE (Perspective API)

provider = "perspective"
api_key = os.getenv("PERSPECTIVE_API_KEY")

if provider == "perspective":
    import requests

    client = requests.Session()


def moderate_batch(
    messages: List[str],
    categories: List[str] = ["harassment"],
    threshold: float | None = None,
) -> List[Dict[str, any]]:
    """
    Parameters
    ----------
    messages: List[str]
        List of user texts to moderate.
    categories: List[str]
        Policy categories to evaluate (default: harassment).
    threshold: float | None
        Decision threshold; if provided, only unsafe results >= threshold are returned.

    Returns
    -------
    List[Dict[str, any]]
        Each dict contains: unsafe, category, score, span.
    """
    results = []
    for text in messages:
        request = ModerationRequest(
            text=text, category=categories[0], threshold=threshold
        )
        raw = moderate_text(provider, request)
        results.append(
            {
                "unsafe": raw.unsafe,
                "category": raw.category,
                "score": raw.score,
                "span": raw.span,
            }
        )
    return results
