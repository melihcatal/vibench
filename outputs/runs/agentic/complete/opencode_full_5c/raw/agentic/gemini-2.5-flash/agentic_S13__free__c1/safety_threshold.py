import os
import json
from typing import Dict
from safety_models import TextModerationResponse, ModerationCategory
from safety_client import GoogleSafetyClient


def apply_safety_thresholds(
    moderation_response: TextModerationResponse,
    threshold_secret_id: str = "moderation_thresholds",
) -> TextModerationResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    client = GoogleSafetyClient(project_id, location)

    try:
        threshold_json = client.get_secret_version(threshold_secret_id)
        thresholds: Dict[str, float] = json.loads(threshold_json)
    except Exception as e:
        print(
            f"Could not retrieve thresholds from Secret Manager: {e}. Using default thresholds."
        )
        # Default thresholds if Secret Manager fails or is not configured
        thresholds = {
            "HATE_SPEECH": 0.7,
            "SEXUALLY_EXPLICIT": 0.8,
            "HARASSMENT": 0.6,
            "DANGEROUS_CONTENT": 0.85,
            "OFFENSIVE_TERMS": 0.9,
            "PERSONAL_IDENTIFIABLE_INFORMATION": 0.9,
        }

    updated_categories: list[ModerationCategory] = []
    overall_safe = True
    decision_reasons = []

    for category_data in moderation_response.categories:
        category_name = category_data.category
        score = category_data.score
        threshold = thresholds.get(category_name, 0.5)  # Default to 0.5 if not found

        allowed = score < threshold
        updated_categories.append(
            ModerationCategory(
                category=category_name,
                score=score,
                threshold=threshold,
                allowed=allowed,
            )
        )

        if not allowed:
            overall_safe = False
            decision_reasons.append(
                f"{category_name} exceeded threshold ({score:.2f} >= {threshold:.2f})."
            )

    return TextModerationResponse(
        filtered_text=moderation_response.filtered_text,
        categories=updated_categories,
        is_safe=overall_safe,
        decision_reason=" ".join(decision_reasons).strip()
        or "Text is safe based on thresholds.",
    )
