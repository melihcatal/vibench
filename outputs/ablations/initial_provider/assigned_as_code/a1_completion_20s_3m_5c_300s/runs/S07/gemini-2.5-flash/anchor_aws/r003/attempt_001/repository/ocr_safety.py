import boto3
from document_client import get_comprehend_client


def ocr_safety(payload, config=None):
    config = config or {}
    client = get_comprehend_client(region_name=config.get("region"))
    text_to_analyze = payload["text"]

    # Detect dominant language first to use for content moderation
    detect_language_response = client.detect_dominant_language(Text=text_to_analyze)
    dominant_language_code = detect_language_response["Languages"][0]["LanguageCode"]

    # Use detect_sentiment to get a general idea, and also PII detection could be considered for safety
    # For more advanced content moderation, a custom Comprehend model or Rekognition for images might be used
    # For this exercise, we will use detect_sentiment and detect_pii_entities as proxies for safety.
    sentiment_response = client.detect_sentiment(
        Text=text_to_analyze, LanguageCode=dominant_language_code
    )
    pii_response = client.detect_pii_entities(
        Text=text_to_analyze, LanguageCode=dominant_language_code
    )

    safety_assessment = {
        "sentiment": sentiment_response["Sentiment"],
        "sentiment_score": sentiment_response["SentimentScore"],
        "pii_entities_count": len(pii_response["Entities"]),
        "pii_entities": pii_response["Entities"],
    }

    return safety_assessment
