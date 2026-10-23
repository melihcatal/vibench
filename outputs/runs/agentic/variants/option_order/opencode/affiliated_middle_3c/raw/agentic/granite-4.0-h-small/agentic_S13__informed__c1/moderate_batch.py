# [SAME-SCENARIO] moderate_batch.py
# Moderates a batch of user messages and returns per-message decisions

from typing import List, Dict
from safety_client import TextSafetyClient


def moderate_batch(texts: List[str], **kwargs) -> List[Dict]:
    """Send a list of texts to the configured safety service and return a list of decisions.

    Args:
        texts: List of user messages to evaluate.
        **kwargs: Forwarded to the underlying client (e.g., batch_size, thresholds).

    Returns:
        A list of dicts, each matching the format of `moderate_text.score_text` for the corresponding text.
    """
    client = TextSafetyClient()
    responses = client.analyze_batch(texts, **kwargs)
    normalized = []
    for resp in responses:
        normalized.append(
            {
                "unsafe": resp.get("unsafe", False),
                "reason": resp.get("reason", "No unsafe content detected."),
                "score": resp.get("score"),
            }
        )
    return normalized
