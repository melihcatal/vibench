import boto3

from safety_client import get_comprehend_client
from safety_models import format_threshold_request, parse_threshold_response


def safety_threshold(payload, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    request = format_threshold_request(payload)
    response = client.detect_toxic_content(request)
    return parse_threshold_response(response)