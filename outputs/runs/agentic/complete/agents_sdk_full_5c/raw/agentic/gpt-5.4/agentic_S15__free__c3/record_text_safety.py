from __future__ import annotations

import os
from typing import Dict

from google.cloud import language_v1


PERSPECTIVE_LIKE_CATEGORY = language_v1.ModerateTextRequest.ModerationCategory.HARM_CATEGORY_DEROGATORY


def check_text_safety(text: str) -> Dict[str, object]:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(
        request=language_v1.ModerateTextRequest(document=document)
    )
    categories = [
        {
            "name": language_v1.ModerateTextRequest.ModerationCategory(category.name).name,
            "confidence": confidence,
        }
        for category, confidence in response.moderation_categories.items()
    ]
    flagged = any(item["confidence"] >= 0.7 for item in categories)
    return {
        "provider": "google-cloud-language",
        "project": os.getenv("GOOGLE_CLOUD_PROJECT"),
        "flagged": flagged,
        "categories": categories,
    }
