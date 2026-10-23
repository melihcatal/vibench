from typing import Dict, List
from safety_models import SafetyCategory, ModerationResponse


def apply_safety_threshold(moderation_result: ModerationResponse) -> bool:
    category_thresholds = {
        SafetyCategory.HATE_SPEECH: 0.7,
        SafetyCategory.SEXUALLY_EXPLICIT: 0.8,
        SafetyCategory.DANGEROUS_CONTENT: 0.75,
        SafetyCategory.HARASSMENT: 0.7,
    }

    for category in moderation_result["categories"]:
        category_name = category["name"]
        confidence = category["confidence"]

        for safety_category, threshold in category_thresholds.items():
            if safety_category.value == category_name and confidence >= threshold:
                return False

    return True
