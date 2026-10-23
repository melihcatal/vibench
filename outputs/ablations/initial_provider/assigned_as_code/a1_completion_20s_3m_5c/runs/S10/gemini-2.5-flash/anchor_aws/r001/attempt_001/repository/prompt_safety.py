import boto3


def prompt_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload["text"]
    
    # Example of using Comprehend for safety - detecting sentiment and language
    # More advanced safety checks would involve custom moderation or other services
    
    # Detect dominant language (useful for understanding text before analysis)
    detect_language_response = client.detect_dominant_language(Text=text)
    languages = detect_language_response.get("Languages", [])
    dominant_language_code = languages[0]["LanguageCode"] if languages else "en"

    # Detect sentiment to get an idea of the text's emotional tone
    detect_sentiment_response = client.detect_sentiment(
        Text=text,
        LanguageCode=dominant_language_code  # Use the detected language
    )
    sentiment = detect_sentiment_response.get("Sentiment")
    sentiment_score = detect_sentiment_response.get("SentimentScore", {})

    is_safe = True
    reasons = []

    if sentiment in ["NEGATIVE", "MIXED"] and (
        sentiment_score.get("Negative", 0) > 0.7 or sentiment_score.get("Mixed", 0) > 0.7
    ): # Arbitrary threshold for demonstration
        is_safe = False
        reasons.append(f"Potentially negative/mixed sentiment detected: {sentiment}")
    
    # Further checks would integrate with more specific content moderation services or custom logic.
    
    return {"is_safe": is_safe, "reasons": reasons, "sentiment": sentiment}
