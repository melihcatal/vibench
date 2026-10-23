import boto3

from safety_client import get_comprehend_client
from safety_models import format_audio_request, parse_audio_response


def reviewer_brief_audio(payload, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    request = format_audio_request(payload)
    response = client.generate_audio_brief(request)
    return parse_audio_response(response)