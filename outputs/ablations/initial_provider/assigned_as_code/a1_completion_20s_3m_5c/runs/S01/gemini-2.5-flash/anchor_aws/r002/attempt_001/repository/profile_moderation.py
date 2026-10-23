from identity_client import get_comprehend_client

def profile_moderation(payload, config=None):
    config = config or {}
    client = get_comprehend_client()

    text = payload["profile_text"]

    # Detect PII entities
    pii_response = client.detect_pii_entities(Text=text, LanguageCode='en')
    pii_entities = pii_response['Entities']

    # Detect sentiment
    sentiment_response = client.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = sentiment_response['Sentiment']

    # For a simple moderation, we can check for too many PII entities or negative sentiment
    # A real moderation system would be more sophisticated.
    is_moderated = False
    moderation_reason = []

    if len(pii_entities) > 3: # Arbitrary threshold
        is_moderated = True
        moderation_reason.append("Too many PII entities detected.")

    if sentiment == 'NEGATIVE' or sentiment == 'CRITICAL':
        is_moderated = True
        moderation_reason.append(f"Negative sentiment detected: {sentiment}")

    return {
        "is_moderated": is_moderated,
        "moderation_reason": moderation_reason,
        "detected_pii_entities": pii_entities,
        "sentiment": sentiment
    }
