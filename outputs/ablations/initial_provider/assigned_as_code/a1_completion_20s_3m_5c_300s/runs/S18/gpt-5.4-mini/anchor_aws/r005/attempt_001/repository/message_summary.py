import boto3


def message_summary(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload.get("text") or payload.get("message") or ""
    sentiment = client.detect_sentiment(Text=text, LanguageCode=config.get("language_code", "en"))
    return {"sentiment": sentiment.get("Sentiment"), "sentiment_score": sentiment.get("SentimentScore", {})}
