import boto3


def summarize_message(results):
    client = boto3.client("comprehend", region_name="us-east-1")
    if isinstance(results, str):
        text = results
    else:
        text = " ".join(str(x) for x in results)
    response = client.detect_sentiment(Text=text[:4500], LanguageCode="en")
    return {"provider": "aws-comprehend", "sentiment": response.get("Sentiment", "UNKNOWN"), "sentiment_score": response.get("SentimentScore", {})}
