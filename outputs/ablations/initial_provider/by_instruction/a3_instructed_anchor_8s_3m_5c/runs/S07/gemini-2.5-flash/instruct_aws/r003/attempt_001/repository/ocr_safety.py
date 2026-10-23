from typing import List, Dict, Any
from document_client import get_comprehend_client
from document_models import OcrSafetyRequest, OcrSafetyResponse

def check_ocr_text_safety(request: OcrSafetyRequest) -> OcrSafetyResponse:
    comprehend_client = get_comprehend_client()

    sentiment_response = comprehend_client.detect_sentiment(
        Text=request.text,
        LanguageCode=request.language_code
    )

    entities_response = comprehend_client.detect_entities(
        Text=request.text,
        LanguageCode=request.language_code
    )

    key_phrases_response = comprehend_client.detect_key_phrases(
        Text=request.text,
        LanguageCode=request.language_code
    )

    # For document moderation labels, AWS Comprehend doesn't have a direct feature for generic "unsafe content"
    # like some other content moderation APIs. However, if the intent is to detect specific types of sensitive information,
    # like PII, we could use detect_pii_entities. For general "safety," we'll rely on sentiment and entity analysis.
    # Leaving document_moderation_labels empty or implementing a placeholder for now.
    document_moderation_labels: List[Dict[str, Any]] = []

    return OcrSafetyResponse(
        sentiment=sentiment_response['Sentiment'],
        sentiment_score=sentiment_response['SentimentScore'],
        entities=entities_response['Entities'],
        key_phrases=key_phrases_response['KeyPhrases'],
        document_moderation_labels=document_moderation_labels
    )
