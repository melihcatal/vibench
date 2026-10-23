import boto3


def vendor_text_safety(text):
    client = boto3.client("comprehend")
    result = client.detect_sentiment(Text=text[:4500], LanguageCode="en")
    return {
        "provider": "aws-comprehend",
        "sentiment": result.get("Sentiment"),
        "scores": result.get("SentimentScore", {}),
    }
