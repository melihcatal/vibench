# HELPER: safety_models.py
"""Local request/response and normalization helpers for the Text Content Safety API."""

from typing import Dict, Any, List

# ---------------------------------------------------------------------------
# Request construction helpers
# ---------------------------------------------------------------------------


def build_moderation_request(texts: List[str]) -> Dict[str, Any]:
    """Create a payload compliant with the selected provider's moderation endpoint.

    Args:
        texts: List of user messages to evaluate.

    Returns:
        Dict ready to be sent via the client.
    """
    if PROVIDER == "openai":
        # OpenAI moderation endpoint expects a single text per request or a batch
        # Here we build a generic batch payload; the client wrapper can handle splitting
        return {
            "model": "openai/moderation-latest",
            "input": texts,
        }
    elif PROVIDER == "custom":
        # Custom provider shape (illustrative)
        return {
            "messages": [{"content": t} for t in texts],
            "model": "custom-moderator",
        }
    else:
        raise ValueError(f"Unsupported provider {PROVIDER}")


# ---------------------------------------------------------------------------
# Response parsing helpers
# ---------------------------------------------------------------------------


def normalize_moderation_response(raw: Any) -> List[Dict[str, Any]]:
    """Convert provider raw response into a uniform list of category dicts.

    Each dict contains:
        - category name
        - flag (bool) indicating a violation
        - score (float) from 0.0 to 1.0
    """
    if PROVIDER == "openai":
        # OpenAI returns a list of results, each with categories + flagged_content
        results = raw.get("results", [])
        normalized = []
        for res in results:
            categories = res.get("categories", {})
            for cat, meta in categories.items():
                normalized.append(
                    {
                        "category": cat,
                        "flag": meta.get("flagged", False),
                        "score": meta.get("severity_score", 0.0),  # example field
                    }
                )
        return normalized
    elif PROVIDER == "custom":
        # Custom provider returns a flat list of violations
        return [
            {
                "category": v["type"],
                "flag": v["flagged"],
                "score": v["confidence"],
            }
            for v in raw.get("violations", [])
        ]
    else:
        raise ValueError(f"Unsupported provider {PROVIDER}")
