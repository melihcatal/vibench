import os
from google.cloud import language_v1
from typing import Dict, Any


client = language_v1.LanguageServiceClient()


def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.moderate_text(document=document)

    return {
        "is_safe": not any(
            category.severity > language_v1.ModerateTextRequest.HarmSeverity.HARM_SEVERITY_NEGLIGIBLE
            for category in response.moderation_categories
        ),
        "categories_violated": [
            category.name for category in response.moderation_categories
            if category.severity > language_v1.ModerateTextRequest.HarmSeverity.HARM_SEVERITY_NEGLIGIBLE
        ]
    }