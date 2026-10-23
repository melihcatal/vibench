import boto3

from safety_client import get_comprehend_client
from safety_models import format_translate_request, parse_translate_response


def appeal_translate(payload, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    request = format_translate_request(payload)
    response = client.translate_text(request)
    return parse_translate_response(response)