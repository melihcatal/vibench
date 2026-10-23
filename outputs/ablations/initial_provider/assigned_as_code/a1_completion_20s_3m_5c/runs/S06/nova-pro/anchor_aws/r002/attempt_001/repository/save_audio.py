import boto3

from speech_client import get_polly_client
from speech_models import synthesize_speech_request, synthesize_speech_response


def save_audio(audio_bytes, file_path):
    with open(file_path, 'wb') as f:
        f.write(audio_bytes)


def synthesize_speech(payload, config=None):
    config = config or {}
    client = get_polly_client(config)
    request = synthesize_speech_request(payload)
    response = client.synthesize_speech(**request)
    audio_bytes = synthesize_speech_response(response)
    return audio_bytes