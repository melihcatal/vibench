import boto3


def metric_annotation_safety(text):
    client = boto3.client("comprehend")
    result = client.detect_sentiment(Text=text, LanguageCode="en")
    return {"sentiment": result.get("Sentiment"), "scores": result.get("SentimentScore", {})}
