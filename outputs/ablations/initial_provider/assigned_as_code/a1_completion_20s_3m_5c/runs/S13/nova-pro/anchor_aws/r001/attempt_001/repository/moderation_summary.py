import boto3

from safety_client import get_comprehend_client
from safety_models import format_summary_request, parse_summary_response


def moderation_summary(payloads, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    request = format_summary_request(payloads)
    response = client.summarize_moderation(request)
    return parse_summary_response(response)