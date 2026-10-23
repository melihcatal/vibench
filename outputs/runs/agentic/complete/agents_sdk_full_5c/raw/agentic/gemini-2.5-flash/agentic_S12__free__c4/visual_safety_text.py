from google.cloud import language_v1
from typing import Dict, Any
import os

def check_text_for_safety(text: str) -> Dict[str, Any]:
    """
    Checks generated visual labels and descriptions for unsafe text content
    using Google Cloud Natural Language API for sentiment and entity analysis,
    which can indirectly indicate problematic content or use classification
    for explicit content moderation if available.
    For direct content moderation, a dedicated moderation API would be ideal.
    Here, we'll use sentiment as a proxy.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Perform sentiment analysis
    sentiment_response = client.analyze_sentiment(
        request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
    )
    sentiment = sentiment_response.document_sentiment

    # Perform content classification (if the text is long enough and feature is enabled)
    # This requires content classification to be enabled for the project and text to be substantial.
    # For short labels, sentiment is more direct.
    try:
        classification_response = client.classify_text(request={"document": document})
        categories = [{"name": category.name, "confidence": category.confidence} for category in classification_response.categories]
    except Exception as e:
        # Classification might fail for very short texts or if not enabled
        categories = []
        print(f"Warning: Text classification failed for '{text}': {e}")


    safety_check_results = {
        "text_sentiment": {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude,
        },
        "text_categories": categories,
        # Add a simple rule-based flag for "unsafe" based on sentiment
        "is_potentially_unsafe": sentiment.score < -0.5 and sentiment.magnitude > 1.0 # Heuristic
    }
    return safety_check_results
