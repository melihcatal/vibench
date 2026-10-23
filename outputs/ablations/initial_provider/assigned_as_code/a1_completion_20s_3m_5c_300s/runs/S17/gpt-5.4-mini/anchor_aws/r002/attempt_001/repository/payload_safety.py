import boto3


def payload_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload.get("plaintext") or payload.get("text") or ""
    if isinstance(text, bytes):
        text = text.decode(errors="ignore")
    response = client.detect_sentiment(Text=text, LanguageCode=config.get("language_code", "en"))
    return {"sentiment": response.get("Sentiment"), "sentiment_score": response.get("SentimentScore", {})}
