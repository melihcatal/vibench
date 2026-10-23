import boto3

from database_models import normalize_item


def record_text_safety(record):
    comprehend = boto3.client("comprehend", region_name="us-east-1")
    item = normalize_item(record) or {}
    text = str(item.get("body") or item.get("content") or "")
    if not text:
        return {"safe": True, "reason": "empty"}
    response = comprehend.detect_sentiment(Text=text[:5000], LanguageCode="en")
    return {"safe": response.get("Sentiment") not in {"NEGATIVE", "MIXED"}, "sentiment": response.get("Sentiment")}
