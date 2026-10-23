import boto3

from safety_client import get_client
from safety_models import normalize_response


def redact_unsafe(payload, config=None):
    config = config or {}
    client = get_client(config)
    response = client.detect_toxic_content(TextSegments=[{"Text": payload["text"]}], LanguageCode="en")
    redacted_text = payload["text"]
    for result in response["ResultList"]:
        if result["Toxicity"] > 0.5:
            redacted_text = redacted_text.replace(result["Text"], "[REDACTED]")
    return {"redacted_text": redacted_text}