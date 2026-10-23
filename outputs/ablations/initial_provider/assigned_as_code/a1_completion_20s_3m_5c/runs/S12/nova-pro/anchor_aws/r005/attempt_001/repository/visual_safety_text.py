import boto3


def visual_safety_text(text, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    response = client.detect_sentiment(
        Text=text,
        LanguageCode="en",
    )
    return response["Sentiment"] == "NEGATIVE"