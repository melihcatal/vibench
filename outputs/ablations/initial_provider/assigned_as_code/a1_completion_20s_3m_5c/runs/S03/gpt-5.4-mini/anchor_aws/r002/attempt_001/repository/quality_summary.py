import boto3


def quality_summary(payload, config=None):
    client = boto3.client("comprehend", region_name=(config or {}).get("region"))
    text = payload.get("text", "")
    response = client.detect_sentiment(Text=text, LanguageCode=payload.get("language", "en"))
    return {
        "issues": [
            {
                "type": "sentiment",
                "sentiment": response["Sentiment"],
                "scores": response["SentimentScore"],
            }
        ],
        "language": payload.get("language", "en"),
    }
