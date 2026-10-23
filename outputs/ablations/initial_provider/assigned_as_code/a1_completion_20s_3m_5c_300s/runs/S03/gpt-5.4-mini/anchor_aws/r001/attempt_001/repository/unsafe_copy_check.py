import boto3


def unsafe_copy_check(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    response = client.detect_sentiment(Text=payload["text"], LanguageCode=payload["language"])
    return {
        "text": payload["text"],
        "language": payload["language"],
        "sentiment": response.get("Sentiment"),
        "scores": response.get("SentimentScore", {}),
    }
