from google.cloud import language_v1
import os


def check_log_text_safety(text: str) -> dict:
    """Check log message text for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    
    response = client.analyze_sentiment(
        request={"document": document}
    )
    
    safety_check = {
        "toxic": response.document_sentiment.score < -0.5,
        "sentiment_score": response.document_sentiment.score,
        "sentiment_magnitude": response.document_sentiment.magnitude
    }
    
    return safety_check