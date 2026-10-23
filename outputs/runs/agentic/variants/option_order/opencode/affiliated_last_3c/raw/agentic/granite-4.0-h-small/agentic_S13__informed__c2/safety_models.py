# safety_models.py
# HELPER implementation
# Data structures for request/response normalization

from typing import Any, Dict, List

# Request model for Alibaba Content Moderation
ModerationRequestParams = Dict[str, Any]

# Example response (fields may differ per provider)
ModerationResponse = Dict[str, Any]

# Normalization helper to extract unsafe spans from a provider response
# Adjust keys to match the concrete provider's actual response shape


def normalize_unsafe_spans(response: ModerationResponse) -> List[Dict[str, Any]]:
    """Convert provider-specific response to list of unsafe span dicts.

    Each dict contains 'start', 'end', and 'category'.
    """
    spans = []
    # Alibaba example expects 'data.locations' list of objects with start/end/category
    if "data" in response and "locations" in response["data"]:
        for loc in response["data"]["locations"]:
            spans.append(
                {
                    "start": loc.get("start"),
                    "end": loc.get("end"),
                    "category": loc.get("category"),
                }
            )
    return spans


# Example normalization of scores (convert to dict of floats)


def normalize_scores(response: ModerationResponse) -> Dict[str, float]:
    scores = {}
    # Alibaba returns a 'scores' dict with numeric confidence per category
    if "scores" in response:
        for k, v in response["scores"].items():
            scores[k] = float(v)
    return scores
