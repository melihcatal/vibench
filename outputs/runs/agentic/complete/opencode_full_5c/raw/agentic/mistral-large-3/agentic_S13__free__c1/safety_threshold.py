from typing import Dict, List
from safety_client import SafetyClient
from safety_models import ModerationCategory


def apply_safety_threshold(
    text: str, custom_thresholds: Dict[ModerationCategory, float] = None
) -> Dict:
    client = SafetyClient()
    default_thresholds = {
        ModerationCategory.HATE_SPEECH: 0.7,
        ModerationCategory.DANGEROUS_CONTENT: 0.8,
        ModerationCategory.HARASSMENT: 0.75,
        ModerationCategory.SEXUALLY_EXPLICIT: 0.8,
    }

    thresholds = custom_thresholds or default_thresholds
    moderation_data = client.moderate_text_content(text)
    if not moderation_data:
        return {"is_allowed": False, "flagged_categories": ["moderation_failed"]}

    moderation_scores = moderation_data["moderation_scores"]
    flagged_categories = []
    for category, threshold in thresholds.items():
        if moderation_scores[category.value] >= threshold:
            flagged_categories.append(category)

    return {
        "is_allowed": len(flagged_categories) == 0,
        "flagged_categories": [cat.value for cat in flagged_categories],
        "scores": moderation_scores,
    }
