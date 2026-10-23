import boto3


def summarize_translation_quality(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload["text"]
    response = client.detect_sentiment(
        Text=text,
        LanguageCode=payload["language_code"],
    )
    return {
        "sentiment": response["Sentiment"],
        "sentiment_score": response["SentimentScore"],
    }