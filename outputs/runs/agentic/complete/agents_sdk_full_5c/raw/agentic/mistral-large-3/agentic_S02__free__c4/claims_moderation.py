from google.cloud import language_v1
from typing import Dict

def moderate_claims(text: str) -> Dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )
    response = client.moderate_text(document=document)

    moderation_result = {
        "language": response.language,
        "moderation_categories": [],
    }

    for category in response.moderation_categories:
        moderation_result["moderation_categories"].append({
            "name": category.name,
            "confidence": category.confidence,
        })

    return moderation_result