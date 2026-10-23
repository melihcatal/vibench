from typing import Dict, Any, List
from google.cloud import language_v1
import os

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "your-google-credentials.json")

client = language_v1.LanguageServiceClient()

def check_text_safety(text: str) -> Dict[str, Any]:
    """
    Checks text for unsafe content using Google Cloud Natural Language API.
    """
    document = language_v1.Document(
        content=text, 
        type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(request={"document": document})
    
    # Check for toxic content using sentiment magnitude as a proxy
    is_toxic = response.document_sentiment.magnitude > 0.8
    
    return {
        "is_toxic": is_toxic,
        "sentiment_score": response.document_sentiment.score,
        "sentiment_magnitude": response.document_sentiment.magnitude
    }

def check_document_safety(document: Dict[str, Any], text_fields: List[str]) -> Dict[str, Any]:
    """
    Checks user-generated document fields for unsafe content.
    """
    results = {}
    for field in text_fields:
        if field in document:
            results[field] = check_text_safety(str(document[field]))
    return results