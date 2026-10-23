from typing import Dict

from safety_client import moderation_threshold


def safety_threshold(categories: Dict[str, float]) -> bool:
    threshold = moderation_threshold()
    return all(score < threshold for score in categories.values())
