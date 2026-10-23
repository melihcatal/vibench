from typing import Dict, List, Optional
import os
from google.cloud import language_v1
from document_models import OCRResponse


def check_unsafe_content(text: str) -> Dict[str, bool]:
    """Check extracted document text for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
    )

    # Check for toxic content using sentiment analysis as a proxy
    unsafe = response.document_sentiment.score < -0.5

    return {"is_unsafe": unsafe, "toxicity_score": response.document_sentiment.score}


def ocr_safety(ocr_response: OCRResponse) -> Dict[str, bool]:
    """Check extracted document text for unsafe content."""
    return check_unsafe_content(ocr_response.text)
