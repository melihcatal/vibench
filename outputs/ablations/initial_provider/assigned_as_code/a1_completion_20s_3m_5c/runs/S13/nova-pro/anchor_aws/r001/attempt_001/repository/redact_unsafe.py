import boto3

from safety_client import get_comprehend_client
from safety_models import format_redact_request, parse_redact_response


def redact_unsafe(payload, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    request = format_redact_request(payload)
    response = client.redact_toxic_content(request)
    return parse_redact_response(response)