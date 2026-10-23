import boto3


def record_summary(payload, config=None):
    client = boto3.client("comprehend", region_name=(config or {}).get("region"))
    text = payload.get("text") or payload.get("document", {}).get("summary") or ""
    response = client.detect_sentiment(Text=text, LanguageCode=payload.get("language_code", "en"))
    return {"sentiment": response.get("Sentiment"), "scores": response.get("SentimentScore", {})}
