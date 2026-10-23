from safety_client import get_perspective_service
from safety_models import normalize_perspective
from typing import Dict, Optional


def safety_threshold(
    text: str, category_thresholds: Optional[Dict[str, float]] = None
) -> bool:
    if category_thresholds is None:
        category_thresholds = {
            "toxicity": 0.7,
            "insult": 0.7,
            "threat": 0.7,
            "sexually_explicit": 0.7,
        }
    service = get_perspective_service()
    if service is None:
        raise ValueError("Perspective API key not configured")
    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
        },
    }
    response = service.comments().analyze(body=analyze_request).execute()
    decision = normalize_perspective(response)
    for category, score in decision.categories.items():
        if category in category_thresholds and score > category_thresholds[category]:
            return False
    return True
