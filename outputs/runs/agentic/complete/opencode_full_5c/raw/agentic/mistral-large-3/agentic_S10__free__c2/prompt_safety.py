import os
from typing import Dict, Any
from google.cloud import language_v1


def check_prompt_safety(text: str) -> Dict[str, Any]:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(request={"document": document})

    sentiment = response.document_sentiment

    return {
        "is_safe": sentiment.score >= -0.5 and sentiment.magnitude <= 0.8,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "provider": "google-cloud-natural-language",
    }
