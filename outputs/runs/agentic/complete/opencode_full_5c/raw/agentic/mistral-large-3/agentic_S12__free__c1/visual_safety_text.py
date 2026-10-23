import os
from google.cloud import language_v1
from typing import Dict, List
from .vision_models import VisualSafetyTextRequest


def analyze_text_safety(request: VisualSafetyTextRequest) -> Dict[str, bool]:
    """Checks generated visual labels and detected text for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    text_content = " ".join(request.labels + [request.detected_text])

    if not text_content.strip():
        return {"is_safe": True, "reason": "No text content to analyze"}

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(request={"document": document})

    sentiment = response.document_sentiment

    response = client.moderate_text(request={"document": document})

    unsafe_categories = [
        category.name
        for category in response.moderation_categories
        if category.confidence > 0.7
    ]

    return {
        "is_safe": not unsafe_categories,
        "unsafe_categories": unsafe_categories,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
    }
