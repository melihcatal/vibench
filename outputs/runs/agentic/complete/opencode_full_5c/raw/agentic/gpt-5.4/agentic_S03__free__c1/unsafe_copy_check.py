from __future__ import annotations

from typing import Any, Dict

from google.cloud import language_v2


def unsafe_copy_check(text: str, language_code: str = "en") -> Dict[str, Any]:
    client = language_v2.LanguageServiceClient()
    document = {
        "content": text,
        "type_": language_v2.Document.Type.PLAIN_TEXT,
        "language_code": language_code,
    }
    response = client.moderate_text(document=document)
    return {
        "provider": "Google Cloud Natural Language",
        "categories": [
            {
                "name": category.name,
                "confidence": category.confidence,
            }
            for category in response.moderation_categories
        ],
    }
