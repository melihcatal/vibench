import boto3

from safety_client import get_client
from safety_models import normalize_response


def moderation_summary(payloads, config=None):
    config = config or {}
    client = get_client(config)
    responses = []
    for payload in payloads:
        response = client.detect_toxic_content(TextSegments=[{"Text": payload["text"]}], LanguageCode="en")
        responses.append(normalize_response(response))
    summary = {"total_messages": len(payloads), "toxic_messages": sum(1 for r in responses if r["toxicity"] > 0.5)}
    return summary