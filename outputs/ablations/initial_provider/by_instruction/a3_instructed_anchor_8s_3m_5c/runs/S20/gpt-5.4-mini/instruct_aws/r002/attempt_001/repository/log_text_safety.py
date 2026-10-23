import boto3


def log_text_safety(text, language_code="en"):
    client = boto3.client("comprehend")
    response = client.detect_sentiment(Text=text, LanguageCode=language_code)
    return {"sentiment": response.get("Sentiment"), "scores": response.get("SentimentScore", {})}
