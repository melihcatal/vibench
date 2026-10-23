import boto3

from safety_client import get_comprehend_client
from safety_models import normalize_payload, parse_response


def redact_unsafe(payload, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    normalized_payload = normalize_payload(payload)
    response = client.detect_toxic_content(TextSegments=[normalized_payload], LanguageCode="en")
    redacted_text = parse_response(response, redact=True)
    return redacted_text