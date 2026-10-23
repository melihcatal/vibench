import json

import boto3


def platform_output_safety(text: str):
    client = boto3.client("comprehend", region_name=(boto3.session.Session().region_name or "us-east-1"))
    response = client.detect_sentiment(Text=text[:5000], LanguageCode="en")
    return {"unsafe": response.get("Sentiment") in {"NEGATIVE", "MIXED"}, "raw": response}
