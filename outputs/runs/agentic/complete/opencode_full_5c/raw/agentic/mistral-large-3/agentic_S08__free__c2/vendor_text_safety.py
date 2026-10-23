from typing import Optional
from google.cloud import language_v1
import os


def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    """Moderate vendor notes or memo fields using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(request={"document": document})
    sentiment = response.document_sentiment

    response_moderation = client.moderate_text(request={"document": document})

    moderation_result = {
        "is_safe": True,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "moderation_categories": {},
    }

    for category in response_moderation.moderation_categories:
        moderation_result["moderation_categories"][category.name] = category.confidence
        if category.confidence > 0.7:
            moderation_result["is_safe"] = False

    return moderation_result
