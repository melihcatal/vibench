import json

from messaging_client import get_comprehend_client

def check_message_safety(text_content: str, language_code: str = "en", region_name: str = None):
    comprehend_client = get_comprehend_client(region_name)

    # Detect PII entities
    pii_response = comprehend_client.detect_pii_entities(
        Text=text_content,
        LanguageCode=language_code
    )
    pii_entities = pii_response["Entities"]

    # Detect dominant language to ensure proper processing
    dominant_language_response = comprehend_client.detect_dominant_language(
        Text=text_content
    )
    detected_language_code = dominant_language_response["Languages"][0]["LanguageCode"]

    # Detect sentiment for potential toxicity/negative content
    sentiment_response = comprehend_client.detect_sentiment(
        Text=text_content,
        LanguageCode=detected_language_code
    )
    sentiment = sentiment_response["Sentiment"]
    sentiment_scores = sentiment_response["SentimentScore"]

    is_unsafe = False
    safety_concerns = []

    if pii_entities:
        is_unsafe = True
        safety_concerns.append("Personally Identifiable Information (PII) detected.")
    
    # Example: Mark as unsafe if sentiment is 'Negative' with a high score
    if sentiment == "NEGATIVE" and sentiment_scores["Negative"] > 0.8:
        is_unsafe = True
        safety_concerns.append("Highly negative sentiment detected.")

    return {
        "is_unsafe": is_unsafe,
        "safety_concerns": safety_concerns,
        "pii_entities_count": len(pii_entities),
        "sentiment": sentiment,
        "detected_language": detected_language_code
    }
