import boto3


def summarize_quality_issues(text: str, aws_region: str | None = None) -> dict[str, object]:
    comprehend = boto3.client("comprehend", region_name=aws_region)
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    return {"provider": "aws-comprehend", "sentiment": sentiment.get("Sentiment"), "sentiment_scores": sentiment.get("SentimentScore", {})}
