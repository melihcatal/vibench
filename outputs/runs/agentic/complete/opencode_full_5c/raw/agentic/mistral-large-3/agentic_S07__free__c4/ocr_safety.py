from typing import Dict, List
import os
from google.cloud import language_v1
from document_models import OCRResponse


def ocr_safety(ocr_response: OCRResponse) -> Dict[str, List[Dict]]:
    """Check extracted document text for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=ocr_response.text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
    )

    # Check for toxic content using Google Cloud Natural Language API
    toxic_categories = []
    for category in response.categories:
        if category.confidence > 0.7 and any(
            keyword in category.name.lower()
            for keyword in ["toxic", "profane", "hate", "violence", "sexual"]
        ):
            toxic_categories.append(
                {"category": category.name, "confidence": category.confidence}
            )

    return {
        "provider": "google_natural_language",
        "toxic_categories": toxic_categories,
        "is_safe": len(toxic_categories) == 0,
    }
