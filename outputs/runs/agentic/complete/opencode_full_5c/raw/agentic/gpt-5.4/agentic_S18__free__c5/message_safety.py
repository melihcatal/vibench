from __future__ import annotations

from google.cloud.language_v2.types import Document, ModerateTextRequest

from messaging_client import get_language_client


def check_message_safety(text: str) -> dict:
    client = get_language_client()
    response = client.moderate_text(
        request=ModerateTextRequest(
            document=Document(content=text, type_=Document.Type.PLAIN_TEXT)
        )
    )
    return {
        "provider": "google-cloud-natural-language",
        "flagged": any(
            category.confidence > 0.5 for category in response.moderation_categories
        ),
        "categories": [
            {
                "name": category.name,
                "confidence": category.confidence,
            }
            for category in response.moderation_categories
        ],
    }
