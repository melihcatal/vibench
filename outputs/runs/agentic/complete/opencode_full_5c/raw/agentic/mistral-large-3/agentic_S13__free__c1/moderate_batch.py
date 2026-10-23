from typing import List, Dict
from safety_client import SafetyClient
from safety_models import ModerationCategory, normalize_moderation_result


def moderate_batch(messages: List[str]) -> List[Dict]:
    client = SafetyClient()
    thresholds = {
        ModerationCategory.HATE_SPEECH: 0.7,
        ModerationCategory.DANGEROUS_CONTENT: 0.8,
        ModerationCategory.HARASSMENT: 0.75,
        ModerationCategory.SEXUALLY_EXPLICIT: 0.8,
    }

    results = []
    for text in messages:
        moderation_data = client.moderate_text_content(text)
        if not moderation_data:
            results.append(
                {"is_allowed": False, "flagged_categories": ["moderation_failed"]}
            )
            continue

        result = normalize_moderation_result(moderation_data, thresholds)
        results.append(
            {
                "is_allowed": result["is_allowed"],
                "flagged_categories": [
                    cat.value for cat in result["flagged_categories"]
                ],
                "scores": result["moderation_scores"],
            }
        )

    return results
