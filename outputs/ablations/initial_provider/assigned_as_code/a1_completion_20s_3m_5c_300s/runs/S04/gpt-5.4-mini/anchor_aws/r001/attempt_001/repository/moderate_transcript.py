import boto3


def moderate_transcript(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    response = client.detect_sentiment(Text=payload["text"], LanguageCode=payload.get("language_code", "en"))
    return {
        "sentiment": response["Sentiment"],
        "sentiment_scores": response["SentimentScore"],
        "approved": response["Sentiment"] in {"POSITIVE", "NEUTRAL"},
    }
