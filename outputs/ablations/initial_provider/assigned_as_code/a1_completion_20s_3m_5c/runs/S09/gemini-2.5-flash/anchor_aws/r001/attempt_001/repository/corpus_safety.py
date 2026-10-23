import boto3

def corpus_safety_check(text, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region", "us-east-1"))
    
    # Detect PII entities
    pii_response = client.detect_pii_entities(Text=text, LanguageCode="en")
    pii_entities = pii_response["Entities"]
    
    # Detect sentiment (as a general safety indicator)
    sentiment_response = client.detect_sentiment(Text=text, LanguageCode="en")
    sentiment = sentiment_response["Sentiment"]
    
    # You can add more comprehensive checks here, e.g., custom content moderation models
    
    is_safe = True
    safety_flags = []

    if pii_entities:
        is_safe = False
        safety_flags.append("PII_DETECTED")

    if sentiment in ["NEGATIVE", "MIXED"]:
        # This is a simplified safety check; actual safety might involve more nuanced sentiment analysis
        # or topic detection for harmful content.
        safety_flags.append(f"SENTIMENT_{sentiment.upper()}")

    return {"is_safe": is_safe, "safety_flags": safety_flags, "pii_entities": pii_entities, "sentiment": sentiment}
