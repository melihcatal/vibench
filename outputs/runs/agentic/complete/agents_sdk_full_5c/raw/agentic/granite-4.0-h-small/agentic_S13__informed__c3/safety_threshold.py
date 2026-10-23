import os
import json
from safety_client import SafetyClient
from safety_models import SafetyModels

def apply_thresholds(text: str, thresholds: dict) -> bool:
    """Determine whether text passes safety thresholds.
    thresholds: dict mapping category -> max_score (e.g., {'hate': 0.5, 'self_harm': 0.3})
    Uses Azure AI Content Safety scores (0‑1) and returns True if all categories stay below the limit.
    """
    client = SafetyClient()
    payload = SafetyModels.build_payload(text)
    raw = client.detect(text)
    normalized = SafetyModels.normalize_response(raw)
    categories = normalized.get('categories', [])
    for cat in categories:
        name = cat['name']
        score = cat['score']
        limit = thresholds.get(name, 1.0)
        if score > limit:
            return False
    return True

if __name__ == "__main__":
    test_text = "Hate speech example."
    thresholds = {"hate": 0.4, "self_harm": 0.2}
    print(apply_thresholds(test_text, thresholds))
