import boto3


def platform_output_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region", "us-east-1"))
    text = payload["text"]
    sentiment = client.detect_sentiment(Text=text, LanguageCode=config.get("language_code", "en"))
    unsafe = sentiment.get("Sentiment") in {"NEGATIVE", "MIXED"} and sentiment.get("SentimentScore", {}).get("Negative", 0) > 0.8
    return {"safe": not unsafe, "analysis": sentiment}
