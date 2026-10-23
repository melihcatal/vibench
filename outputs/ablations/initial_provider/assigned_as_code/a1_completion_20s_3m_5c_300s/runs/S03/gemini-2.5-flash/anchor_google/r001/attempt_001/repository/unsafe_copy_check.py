import os
from typing import Dict, Any, List
from google.cloud import language_v1
from translation_client import get_project_id # Re-using for project ID
from translation_models import UnsafeContentCheckRequest, UnsafeContentCheckResponse

def check_unsafe_content(payload: UnsafeContentCheckRequest, config: Dict[str, Any] = None) -> UnsafeContentCheckResponse:
    config = config or {}
    project_id = config.get("project_id", get_project_id())
    
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=payload.text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
        language=payload.language
    )

    # Analyze sentiment to get an overall idea of the text's tone
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    
    # Analyze categories to classify the text content
    # This is a good way to identify potentially unsafe content by category.
    # Note: For stricter content moderation, a dedicated moderation API (if available and allowed) would be more suitable.
    response = client.classify_text(request={'document': document})
    
    is_safe = True
    categories_found = []

    # Example: Mark as unsafe if sentiment is very negative or if certain categories are found
    # These thresholds and categories are illustrative and should be tuned for specific needs.
    if sentiment.score < -0.6 and sentiment.magnitude > 1.0: # Very negative sentiment with high magnitude
        is_safe = False
        categories_found.append("Strong Negative Sentiment")

    for category in response.categories:
        categories_found.append(category.name)
        # Example: if a category name implies unsafe content, mark as unsafe.
        # This would require a more sophisticated mapping in a real application.
        if "/Violence" in category.name or "/Hate Speech" in category.name or "/Adult" in category.name:
            is_safe = False

    return UnsafeContentCheckResponse(
        is_safe=is_safe,
        categories=categories_found
    )
