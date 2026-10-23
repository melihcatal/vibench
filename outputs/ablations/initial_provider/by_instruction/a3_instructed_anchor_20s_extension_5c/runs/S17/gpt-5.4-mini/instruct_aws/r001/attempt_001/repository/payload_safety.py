import boto3


def payload_safety(text: str):
    client = boto3.client("comprehend")
    response = client.detect_sentiment(Text=text, LanguageCode="en")
    return {"provider": "aws-comprehend", "sentiment": response.get("Sentiment", "UNKNOWN"), "score": response.get("SentimentScore", {})}
