from security_models import PayloadSafetyConfig
from security_client import get_comprehend_client

def check_payload_safety(text_payload: str, config: PayloadSafetyConfig):
    client = get_comprehend_client(config.aws_region)

    # Detect PII entities
    pii_response = client.detect_pii_entities(Text=text_payload, LanguageCode="en")
    pii_entities = pii_response["Entities"]

    # Detect sentiment (as an indicator of potentially unsafe or abusive language)
    sentiment_response = client.detect_sentiment(Text=text_payload, LanguageCode="en")
    sentiment = sentiment_response["Sentiment"]

    # Detect dominant language
    dominant_language_response = client.detect_dominant_language(Text=text_payload)
    dominant_language = dominant_language_response["Languages"][0]["LanguageCode"]

    is_unsafe = False
    safety_notes = []

    if pii_entities:
        is_unsafe = True
        safety_notes.append("Potential PII detected.")
    
    if sentiment in ["NEGATIVE", "MIXED"]:
        # Further analysis would be needed for actual unsafety, but for this example, we flag negative sentiment
        safety_notes.append(f"Payload sentiment is {sentiment}.")
    
    return {
        "is_unsafe": is_unsafe,
        "safety_notes": safety_notes,
        "pii_entities": pii_entities,
        "sentiment": sentiment,
        "dominant_language": dominant_language,
    }
