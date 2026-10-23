from typing import Dict, Optional
from safety_models import SafetyCategory, ModerationDecision
from moderate_text import moderate_text


def apply_safety_threshold(
    text: str,
    threshold: Dict[SafetyCategory, float],
    categories: Optional[list[SafetyCategory]] = None,
) -> bool:
    """
    Applies category thresholds to decide whether to allow text using Google Content Safety API.
    """
    decision: ModerationDecision = moderate_text(text, categories=categories)
    
    for category, score in decision["scores"].items():
        if score >= threshold.get(category, 0.0):
            return False
    
    return decision["allowed"]