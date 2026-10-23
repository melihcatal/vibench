from google.cloud import language_v1
from typing import Dict, Any

def quality_summary(payload: Dict[str, str], config: Dict[str, Any]) -> Dict[str, Any]:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=payload["translated_text"],
        type_=language_v1.Document.Type.PLAIN_TEXT,
        language=payload["target_language"],
    )
    sentiment = client.analyze_sentiment(request={
        "document": document,
        "encoding_type": language_v1.EncodingType.UTF8
    }).document_sentiment

    return {
        "translated_text": payload["translated_text"],
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "summary": f"Sentiment score: {sentiment.score}, Magnitude: {sentiment.magnitude}"
    }
