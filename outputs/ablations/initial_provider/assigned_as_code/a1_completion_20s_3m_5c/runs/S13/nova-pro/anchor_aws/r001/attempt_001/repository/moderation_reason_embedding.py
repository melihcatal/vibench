import boto3

from safety_client import get_comprehend_client
from safety_models import format_embedding_request, parse_embedding_response


def moderation_reason_embedding(payload, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    request = format_embedding_request(payload)
    response = client.embed_moderation_reason(request)
    return parse_embedding_response(response)