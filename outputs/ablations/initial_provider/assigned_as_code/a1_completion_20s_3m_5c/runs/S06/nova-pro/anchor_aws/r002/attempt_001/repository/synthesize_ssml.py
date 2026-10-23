import boto3

from speech_client import get_polly_client
from speech_models import synthesize_ssml_request, synthesize_ssml_response


def synthesize_ssml(payload, config=None):
    config = config or {}
    client = get_polly_client(config)
    request = synthesize_ssml_request(payload)
    response = client.synthesize_speech(**request)
    return synthesize_ssml_response(response)