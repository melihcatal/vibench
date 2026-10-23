from security_client import get_google_cloud_language_client
from google.cloud.language_v1 import Document, enums, client

def check_secret_label_safety(text: str) -> dict:
    client = get_google_cloud_language_client()
    
    document = Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    
    # Detect sentiment to check for potentially unsafe or negative connotations
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    
    # You can also use client.classify_text for content classification
    # or client.analyze_entity_sentiment for more detailed entity analysis
    
    safety_score = (sentiment.score + 1) / 2 # Normalize score to 0-1 range
    
    is_unsafe = safety_score < 0.3 # Example threshold for unsafe text
    
    return {
        "text": text,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "safety_score": safety_score,
        "is_unsafe": is_unsafe,
        "message": "Text analyzed for safety using Google Cloud Natural Language API."
    }
