from speech_client import get_comprehend_client

def script_safety(payload, config=None):
    config = config or {}
    client = get_comprehend_client(region_name=config.get("region"))
    text = payload["text"]
    
    # Using DetectSentiment as a basic safety check. For more advanced moderation, 
    # AWS Comprehend has content moderation APIs like 'DetectPiiEntities' or custom classification.
    # For this example, we'll just check for overwhelmingly negative sentiment.
    response = client.detect_sentiment(Text=text, LanguageCode="en") # Assuming English for simplicity
    sentiment = response["Sentiment"]
    
    is_safe = True
    unsafe_categories = []

    if sentiment == "NEGATIVE" and response["SentimentScore"]["Negative"] > 0.9:
        is_safe = False
        unsafe_categories.append("negative_sentiment")
    
    # In a real scenario, you'd integrate with more robust content moderation.
    # For demonstration, this is a placeholder.
    
    return {"is_safe": is_safe, "unsafe_categories": unsafe_categories}
