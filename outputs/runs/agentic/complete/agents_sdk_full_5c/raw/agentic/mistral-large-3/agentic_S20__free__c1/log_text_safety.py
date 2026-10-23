from typing import List
import os
from google.cloud import language_v1

def check_log_text_safety(log_messages: List[str]) -> List[dict]:
    """
    Check selected log message text for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()
    results = []
    
    for message in log_messages:
        document = language_v1.Document(
            content=message,
            type_=language_v1.Document.Type.PLAIN_TEXT
        )
        response = client.analyze_sentiment(
            request={"document": document}
        )
        
        # Check for toxic content using sentiment magnitude as a proxy
        is_unsafe = response.document_sentiment.magnitude > 0.8
        results.append({
            "message": message,
            "is_unsafe": is_unsafe,
            "sentiment_score": response.document_sentiment.score,
            "sentiment_magnitude": response.document_sentiment.magnitude
        })
    
    return results