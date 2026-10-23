import os
from typing import Dict, Any
from google.cloud import language_v1

def moderate_vendor_text_safety(vendor_notes: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    # The Google Cloud Natural Language API client automatically picks up project ID and credentials
    # from environment variables (e.g., GOOGLE_APPLICATION_CREDENTIALS) or the GKE environment.
    # No explicit project_id or location is usually required for client initialization.
    
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=vendor_notes, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classify text to determine content categories and potential safety issues
    # Note: For explicit content moderation (e.g., harmful categories), the Perspective API or
    # Google Cloud's Vertex AI Safety APIs might be more direct. 
    # The Natural Language API provides more general content categorization.
    response = client.classify_text(request={'document': document})

    categories = [{'name': category.name, 'confidence': category.confidence} for category in response.categories]

    # For a more direct safety check, analyze sentiment and entities to infer potential issues.
    # This is a basic illustration. A production system would integrate with specific safety APIs.
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    sentiment_score = sentiment.score
    sentiment_magnitude = sentiment.magnitude

    safety_check = {
        "text_content": vendor_notes,
        "sentiment_score": sentiment_score,
        "sentiment_magnitude": sentiment_magnitude,
        "categories": categories,
        "is_flagged_for_review": False # Placeholder, logic would be added based on categories/sentiment thresholds
    }

    # Example: Flag if sentiment is very negative or if certain categories appear
    if sentiment_score < -0.5 or any("Violence" in c['name'] for c in categories):
        safety_check["is_flagged_for_review"] = True

    return safety_check
