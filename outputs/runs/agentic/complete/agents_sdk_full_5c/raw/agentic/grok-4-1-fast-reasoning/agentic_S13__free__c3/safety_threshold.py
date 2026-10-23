from typing import Dict, Optional
from safety_client import get_client
from safety_models import normalize_input, DEFAULT_THRESHOLDS

def safety_threshold(
    text: str,
    thresholds: Optional[Dict[str, float]] = None,
) -> bool:
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS
    client = get_client()
    normalized = normalize_input(text)
    response = client.moderations.create(
        model='text-moderation-latest',
        input=normalized,
    )
    result = response.results[0]
    category_scores = dict(result.category_scores)
    for category, thresh in thresholds.items():
        if category in category_scores and category_scores[category] > thresh:
            return False
    return True
