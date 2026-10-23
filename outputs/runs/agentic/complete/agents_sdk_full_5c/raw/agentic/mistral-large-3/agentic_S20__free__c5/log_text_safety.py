from typing import List
import os
from google.cloud import language_v1

def check_log_text_safety(log_messages: List[str]) -> List[dict]:
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
        results.append({
            "message": message,
            "safety_score": response.document_sentiment.score,
            "safety_magnitude": response.document_sentiment.magnitude
        })
    return results