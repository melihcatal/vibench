from google.cloud import language_v1
from document_client import get_google_nl_client
from typing import Dict, Any

def check_safety(text: str) -> Dict[str, Any]:
    """
    Checks extracted document text for unsafe content using Google Cloud Natural Language API.
    This implementation uses sentiment analysis as a basic proxy for content safety.
    For more robust content moderation, dedicated services like Google Cloud's Content Moderation API would be more suitable.
    """
    client = get_google_nl_client()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis
    sentiment_response = client.analyze_sentiment(document=document)
    sentiment = sentiment_response.document_sentiment

    # You can define thresholds for what constitutes "unsafe" based on score and magnitude
    # For example, a very low score might indicate negative or potentially unsafe sentiment.
    is_potentially_unsafe = False
    if sentiment.score < -0.5 and sentiment.magnitude > 1.0: # Arbitrary threshold for demonstration
        is_potentially_unsafe = True

    result = {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "is_potentially_unsafe": is_potentially_unsafe,
        "sentiment_analysis": {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude
        }
    }

    return result
