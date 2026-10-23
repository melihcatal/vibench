import os
from typing import List, Dict, Any
from google.cloud import language_v1

def moderate_batch(texts: List[str]) -> List[Dict[str, Any]]:
    client = language_v1.LanguageServiceClient()
    results = []
    for text_content in texts:
        document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        
        # For simplicity, let's consider highly negative sentiment as potentially unsafe
        is_unsafe = sentiment.score < -0.5  # Example threshold
        
        results.append({
            "text": text_content,
            "is_unsafe": is_unsafe,
            "sentiment_score": sentiment.score,
            "sentiment_magnitude": sentiment.magnitude
        })
    return results
