import boto3

def check_platform_output_safety(text_output, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region", "us-east-1"))
    
    response = client.detect_sentiment(Text=text_output, LanguageCode="en")
    
    sentiment = response["Sentiment"]
    sentiment_score = response["SentimentScore"]
    
    # For the purpose of this exercise, we will consider strongly negative sentiment as potentially "unsafe".
    # In a real-world application, a more sophisticated content moderation service or custom logic would be used.
    is_safe = True
    safety_labels = []
    
    if sentiment == "NEGATIVE" and sentiment_score["Negative"] > 0.8: # Example threshold
        is_safe = False
        safety_labels.append("HIGHLY_NEGATIVE_SENTIMENT")

    return {"is_safe": is_safe, "sentiment": sentiment, "sentiment_score": sentiment_score, "safety_labels": safety_labels}
