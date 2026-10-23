from document_client import get_comprehend_client
from typing import Dict, Any

def moderate_vendor_text(text: str) -> Dict[str, Any]:
    """
    Moderates vendor notes or memo fields using AWS Comprehend.

    Args:
        text: The text string to moderate.

    Returns:
        A dictionary containing moderation results, including sentiment and detected PII.
    """
    comprehend_client = get_comprehend_client()

    sentiment_response = comprehend_client.detect_sentiment(Text=text, LanguageCode='en')
    pii_response = comprehend_client.detect_pii_entities(Text=text, LanguageCode='en')

    # Example of a more advanced moderation would be to check for toxic content using a custom model
    # or a different service like Amazon Rekognition for image-based content moderation.

    moderation_results = {
        "sentiment": sentiment_response.get('Sentiment'),
        "sentiment_score": sentiment_response.get('SentimentScore'),
        "pii_entities": pii_response.get('Entities')
    }

    return moderation_results
