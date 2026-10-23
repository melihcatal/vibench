import boto3


def vendor_text_safety(text: str):
    client = boto3.client("comprehend", region_name="us-east-1")
    moderation = client.detect_sentiment(Text=text, LanguageCode="en")
    return {"provider": "aws-comprehend", "sentiment": moderation.get("Sentiment"), "scores": moderation.get("SentimentScore", {})}
