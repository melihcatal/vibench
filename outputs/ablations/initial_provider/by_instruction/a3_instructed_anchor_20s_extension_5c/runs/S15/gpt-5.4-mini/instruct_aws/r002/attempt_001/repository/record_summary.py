import json

import boto3


def record_summary(document):
    client = boto3.client("comprehend")
    text = json.dumps(document, ensure_ascii=False)
    response = client.detect_sentiment(Text=text[:4500], LanguageCode="en")
    return {"sentiment": response.get("Sentiment"), "sentiment_score": response.get("SentimentScore", {})}
