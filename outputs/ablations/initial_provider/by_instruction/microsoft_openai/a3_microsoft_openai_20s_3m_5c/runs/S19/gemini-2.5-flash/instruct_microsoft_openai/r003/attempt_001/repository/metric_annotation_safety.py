from typing import Dict, Any
from observability_client import ObservabilityClient

def check_annotation_safety(text: str) -> Dict[str, Any]:
    client = ObservabilityClient()

    response = client.comprehend_client.detect_sentiment(
        Text=text,
        LanguageCode='en' # Assuming English for now, can be made dynamic
    )

    # Comprehend also offers detect_dominant_language, detect_entities, etc.
    # For safety, sentiment can indicate potentially negative or alarming language.
    # More sophisticated safety checks would involve custom models or content moderation services.

    sentiment = response.get("Sentiment")
    sentiment_score = response.get("SentimentScore")

    safety_report = {
        "text": text,
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
        "is_potentially_unsafe": sentiment == "NEGATIVE" and sentiment_score.get("Negative", 0.0) > 0.7
        # This is a simplified safety check. Real-world safety would involve more advanced NLP models.
    }

    return safety_report
