import boto3

from safety_client import get_comprehend_client
from safety_models import format_batch_request, parse_batch_response


def moderate_batch(payloads, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    request = format_batch_request(payloads)
    response = client.batch_detect_toxic_content(request)
    return parse_batch_response(response)