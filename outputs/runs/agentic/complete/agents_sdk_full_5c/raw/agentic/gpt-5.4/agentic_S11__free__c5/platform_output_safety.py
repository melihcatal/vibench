from __future__ import annotations

from typing import Any, Dict

from google.cloud import language_v1



def check_platform_output_safety(text: str) -> Dict[str, Any]:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(request={"document": document})
    categories = []
    blocked = False
    for category in response.moderation_categories:
        categories.append(
            {
                "name": category.name,
                "confidence": category.confidence,
                "severity": category.severity,
            }
        )
        if category.confidence >= 0.6:
            blocked = True
    return {"unsafe": blocked, "categories": categories, "provider": "google-cloud-language"}
