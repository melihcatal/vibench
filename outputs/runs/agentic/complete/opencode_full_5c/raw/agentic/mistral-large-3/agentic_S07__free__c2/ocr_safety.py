from typing import Dict, List, Optional
import os
from google.cloud import language_v1
from document_client import get_document_client
from document_models import OCRResponse


def check_unsafe_content(text: str) -> Dict[str, bool]:
    """Check extracted document text for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(request={"document": document})

    # Check for toxic content using sentiment analysis as a proxy
    toxic = response.document_sentiment.score < -0.5

    response = client.moderate_text(request={"document": document})

    return {
        "toxic": toxic,
        "explicit": any(
            category.confidence > 0.7
            for category in response.moderation_categories
            if category.name in ["Toxic", "Insult", "Profanity", "Derogatory"]
        ),
    }


def ocr_safety(image_path: str) -> Dict[str, bool]:
    """Check extracted document text for unsafe content."""
    from extract_text import extract_text

    ocr_result = extract_text(image_path)
    return check_unsafe_content(ocr_result.text)
