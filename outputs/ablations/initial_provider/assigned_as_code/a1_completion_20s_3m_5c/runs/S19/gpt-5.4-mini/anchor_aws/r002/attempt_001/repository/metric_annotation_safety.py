import boto3


def metric_annotation_safety(payload, config=None):
    text = payload.get("text", "")
    client = boto3.client("comprehend", region_name=(config or {}).get("region"))
    response = client.detect_sentiment(Text=text, LanguageCode=payload.get("language", "en"))
    unsafe = response.get("Sentiment") in {"NEGATIVE", "MIXED"} and response.get("SentimentScore", {}).get("Negative", 0) > 0.6
    return {"safe": not unsafe, "sentiment": response.get("Sentiment"), "scores": response.get("SentimentScore", {})}
