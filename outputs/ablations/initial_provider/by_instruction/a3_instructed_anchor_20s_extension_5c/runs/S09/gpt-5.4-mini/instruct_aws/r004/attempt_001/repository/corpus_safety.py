import boto3


def corpus_safety(text):
    client = boto3.client("comprehend")
    result = client.detect_sentiment(Text=text, LanguageCode="en")
    return {"provider": "aws_comprehend", "sentiment": result.get("Sentiment"), "scores": result.get("SentimentScore", {})}
