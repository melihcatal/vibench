import json
from messaging_client import get_comprehend_client

def message_safety(text, config=None):
    config = config or {}
    comprehend_client = get_comprehend_client(config.get("region"))

    # Detect sentiment to get an overall idea of the text's tone
    sentiment_response = comprehend_client.detect_sentiment(Text=text, LanguageCode="en")
    sentiment = sentiment_response["Sentiment"]
    sentiment_score = sentiment_response["SentimentScore"]

    # Detect entities to find specific items in the text that might be sensitive
    entities_response = comprehend_client.detect_entities(Text=text, LanguageCode="en")
    entities = entities_response["Entities"]

    # Detect PII entities for personally identifiable information
    pii_response = comprehend_client.detect_pii_entities(Text=text, LanguageCode="en")
    pii_entities = pii_response["Entities"]

    # Determine if the content is potentially unsafe based on sentiment and presence of PII
    is_unsafe = False
    unsafe_reasons = []

    if sentiment == "NEGATIVE" and sentiment_score["Negative"] > 0.8:
        is_unsafe = True
        unsafe_reasons.append("Strongly negative sentiment")

    if pii_entities:
        is_unsafe = True
        unsafe_reasons.append("Contains Personally Identifiable Information (PII)")

    return {
        "is_unsafe": is_unsafe,
        "reasons": unsafe_reasons,
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
        "entities": entities,
        "pii_entities": pii_entities
    }
