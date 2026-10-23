import boto3


def ocr_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    response = client.detect_sentiment(Text=payload["text"], LanguageCode=payload.get("language", "en"))
    return {"sentiment": response.get("Sentiment"), "sentiment_scores": response.get("SentimentScore", {})}
