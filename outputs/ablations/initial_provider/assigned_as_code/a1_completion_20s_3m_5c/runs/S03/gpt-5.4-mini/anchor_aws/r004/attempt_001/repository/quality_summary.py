import boto3


def quality_summary(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload["text"]
    sentiment = client.detect_sentiment(Text=text, LanguageCode=config.get("language", "en"))
    return {
        "text": text,
        "issues": [sentiment.get("Sentiment")],
        "source_language": payload.get("source_language"),
        "target_language": payload.get("target_language"),
    }
