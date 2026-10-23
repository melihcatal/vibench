import boto3
from security_client import resolve_secret_name


def secret_label_safety() -> dict:
    client = boto3.client("comprehend")
    text = resolve_secret_name("SECRET_LABEL_TEXT", "rotation label")
    result = client.detect_sentiment(Text=text, LanguageCode="en")
    return {"text": text, "safety": result.get("Sentiment", "NEUTRAL")}
