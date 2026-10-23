from __future__ import annotations

from typing import Any, Dict, Optional

from google.cloud import language_v1


def check_platform_output_safety(text: str, project_id: Optional[str] = None) -> Dict[str, Any]:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(document=document)
    categories = []
    for item in response.moderation_categories:
        categories.append(
            {
                "name": item.name,
                "confidence": item.confidence,
                "severity": item.severity,
            }
        )
    return {
        "provider": "google_cloud_natural_language",
        "categories": categories,
    }
