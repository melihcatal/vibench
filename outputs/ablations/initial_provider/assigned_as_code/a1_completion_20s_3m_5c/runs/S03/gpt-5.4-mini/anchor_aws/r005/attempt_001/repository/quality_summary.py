import boto3


def quality_summary(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    response = client.detect_sentiment(Text=payload.get("text", ""), LanguageCode=payload.get("language", "en"))
    return {
        "issues": [response.get("Sentiment", "UNKNOWN")],
        "score": response.get("SentimentScore", {}),
    }
