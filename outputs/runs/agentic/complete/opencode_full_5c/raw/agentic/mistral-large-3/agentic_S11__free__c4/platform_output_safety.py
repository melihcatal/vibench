import os
from typing import Dict, Any

from google.cloud import language_v1
from .model_models import ChatResponse


def platform_output_safety(response: ChatResponse) -> Dict[str, Any]:
    """
    Checks Azure AI Inference model output for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=response.content,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )

    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
    )

    safety_analysis = {
        "sentiment_score": response.document_sentiment.score,
        "sentiment_magnitude": response.document_sentiment.magnitude,
        "unsafe_content_detected": response.document_sentiment.score < -0.5,
        "provider": "google_cloud_natural_language",
    }

    return safety_analysis
