import os
import boto3

def moderate_claims(text: str, language_code: str = "en") -> dict:
    """
    Moderates free-text claims or notes using AWS Comprehend to detect PII and sentiment.
    """
    comprehend = boto3.client('comprehend', region_name=os.environ.get("AWS_REGION"))

    try:
        # Detect PII entities
        pii_response = comprehend.detect_pii_entities(Text=text, LanguageCode=language_code)
        pii_entities = pii_response.get('Entities', [])

        # Detect sentiment
        sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
        sentiment = sentiment_response.get('Sentiment')
        sentiment_score = sentiment_response.get('SentimentScore')

        return {
            "original_text": text,
            "pii_detected": bool(pii_entities),
            "pii_entities": pii_entities,
            "sentiment": sentiment,
            "sentiment_score": sentiment_score
        }
    except Exception as e:
        return {"error": str(e)}
