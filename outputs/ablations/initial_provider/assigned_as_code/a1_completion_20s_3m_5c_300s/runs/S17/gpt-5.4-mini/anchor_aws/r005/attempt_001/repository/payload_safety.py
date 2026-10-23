import boto3

from security_models import normalize_payload


def payload_safety(payload, config=None):
    payload = normalize_payload(payload)
    comprehend = boto3.client("comprehend", region_name=(config or {}).get("region"))
    text = payload.get("plaintext", "")
    response = comprehend.detect_sentiment(Text=text, LanguageCode=payload.get("language", "en"))
    return {"unsafe": response.get("Sentiment") in {"NEGATIVE", "MIXED"}, "sentiment": response.get("Sentiment")}
