import boto3


def platform_output_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region", "us-east-1"))
    response = client.detect_sentiment(Text=payload["text"], LanguageCode=config.get("language", "en"))
    return {"sentiment": response.get("Sentiment"), "sentiment_score": response.get("SentimentScore", {}), "text": payload["text"]}
