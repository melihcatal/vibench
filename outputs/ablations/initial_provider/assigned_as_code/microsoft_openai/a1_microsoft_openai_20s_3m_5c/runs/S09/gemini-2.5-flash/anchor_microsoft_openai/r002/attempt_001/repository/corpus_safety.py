import os
from google.cloud import language_v1
from typing import List, Dict, Any

def corpus_safety(texts: List[str], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    # Google Cloud project ID can be set via GOOGLE_CLOUD_PROJECT environment variable
    # or explicitly passed in config.
    # For this example, we assume GOOGLE_APPLICATION_CREDENTIALS is set up.
    
    client = language_v1.LanguageServiceClient()
    results = []

    for i, text_content in enumerate(texts):
        document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)
        
        try:
            # Performing sentiment analysis as a basic safety check. 
            # A dedicated content moderation API would be more robust for 'safety'.
            sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
            results.append({
                'text_index': i,
                'text': text_content,
                'sentiment_score': sentiment.score,
                'sentiment_magnitude': sentiment.magnitude,
                'is_safe': sentiment.score >= -0.2  # Simple heuristic: consider safe if not strongly negative
            })
        except Exception as e:
            results.append({
                'text_index': i,
                'text': text_content,
                'error': str(e),
                'is_safe': False
            })

    return {'safety_results': results}
