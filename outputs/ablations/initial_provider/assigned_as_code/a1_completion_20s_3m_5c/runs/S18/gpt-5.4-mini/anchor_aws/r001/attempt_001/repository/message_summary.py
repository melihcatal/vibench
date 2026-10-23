import boto3


def message_summary(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload["text"]
    response = client.detect_sentiment(Text=text, LanguageCode=payload.get("language", "en"))
    return {
        "sentiment": response["Sentiment"],
        "sentiment_score": response["SentimentScore"],
        "text_length": len(text),
    }
