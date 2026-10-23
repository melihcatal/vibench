from document_client import get_natural_language_client
from google.cloud import language_v1

def moderate_vendor_text(text: str) -> dict:
    client = get_natural_language_client()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    
    # We are using analyze_sentiment as a proxy for moderation if explicit content moderation API is not available
    # For true moderation, would use Google Cloud Natural Language API's moderateText if it were available
    # Or Perspective API from Google
    response = client.analyze_sentiment(document=document)
    
    # This is a simplified example. Real moderation would involve more detailed classification.
    # Here, we are just returning sentiment score.
    return {
        "text": text,
        "sentiment_score": response.document_sentiment.score,
        "sentiment_magnitude": response.document_sentiment.magnitude,
        "is_safe": response.document_sentiment.score >= -0.5 # Example threshold for "safety"
    }
