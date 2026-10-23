import boto3

from safety_client import get_client
from safety_models import normalize_response


def moderate_batch(payloads, config=None):
    config = config or {}
    client = get_client(config)
    responses = []
    for payload in payloads:
        response = client.detect_toxic_content(TextSegments=[{"Text": payload["text"]}], LanguageCode="en")
        responses.append(normalize_response(response))
    return responses