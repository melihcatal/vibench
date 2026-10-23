import boto3


def vendor_text_safety(payload, config=None):
    client = boto3.client("comprehend", region_name=(config or {}).get("region"))
    text = payload.get("text", "")
    result = client.detect_sentiment(Text=text, LanguageCode=(config or {}).get("language_code", "en"))
    return {"sentiment": result.get("Sentiment"), "scores": result.get("SentimentScore", {})}
