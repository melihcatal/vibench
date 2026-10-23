import boto3


def quality_summary(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload["text"]
    response = client.detect_dominant_language(Text=text)
    return {
        "text": text,
        "language_scores": response.get("Languages", []),
    }
