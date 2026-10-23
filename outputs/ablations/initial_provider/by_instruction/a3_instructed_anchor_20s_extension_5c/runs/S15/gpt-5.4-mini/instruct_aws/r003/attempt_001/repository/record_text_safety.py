from typing import Any, Dict

import boto3


def record_text_safety(record: Dict[str, Any]) -> Dict[str, Any]:
    comprehend = boto3.client("comprehend", region_name="us-east-1")
    text = " ".join(str(value) for value in record.values() if isinstance(value, str))
    sentiment = comprehend.detect_sentiment(Text=text[:4500], LanguageCode="en") if text else {"Sentiment": "NEUTRAL"}
    return {"unsafe": sentiment.get("Sentiment") in {"NEGATIVE", "MIXED"}, "sentiment": sentiment.get("Sentiment")}
