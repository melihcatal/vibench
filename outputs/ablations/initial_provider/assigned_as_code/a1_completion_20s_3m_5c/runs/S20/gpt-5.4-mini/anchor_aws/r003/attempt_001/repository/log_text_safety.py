import boto3


def log_text_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload.get("text", "")
    response = client.detect_sentiment(Text=text, LanguageCode=payload.get("language_code", "en"))
    return {"unsafe": response.get("Sentiment") in {"NEGATIVE", "MIXED"}, "sentiment": response.get("Sentiment")}
