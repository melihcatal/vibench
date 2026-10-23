import boto3

from speech_client import get_polly_client
from speech_models import list_voices_request, list_voices_response


def select_voice(locale, config=None):
    config = config or {}
    client = get_polly_client(config)
    request = list_voices_request(locale)
    response = client.describe_voices(**request)
    return list_voices_response(response)