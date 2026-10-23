import boto3

from database_client import load_config


def record_text_safety(payload, config=None):
    load_config(config)
    comprehend = boto3.client("comprehend")
    text = payload.get("text", "")
    response = comprehend.detect_dominant_language(Text=text)
    return {"safe": bool(response.get("Languages")), "languages": response.get("Languages", [])}
