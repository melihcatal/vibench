import boto3

from safety_client import get_comprehend_client
from safety_models import normalize_payload, parse_response


def moderate_batch(payloads, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    normalized_payloads = [normalize_payload(payload) for payload in payloads]
    responses = client.batch_detect_toxic_content(TextSegments=normalized_payloads, LanguageCode="en")
    return [parse_response(response) for response in responses['ResultList']]