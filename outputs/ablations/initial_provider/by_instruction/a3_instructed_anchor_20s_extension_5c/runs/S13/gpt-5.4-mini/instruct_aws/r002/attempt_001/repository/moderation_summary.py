import boto3


def moderation_summary(decisions):
    client = boto3.client("comprehend", region_name="us-east-1")
    text = " ".join(str(item) for item in decisions)
    response = client.detect_sentiment(Text=text[:4500], LanguageCode="en")
    return {"provider": "aws", "sentiment": response.get("Sentiment"), "summary_score": response.get("SentimentScore", {})}
