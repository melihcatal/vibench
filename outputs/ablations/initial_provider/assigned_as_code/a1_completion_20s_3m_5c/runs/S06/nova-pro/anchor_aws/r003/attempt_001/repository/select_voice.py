import boto3

from speech_client import get_speech_client


def select_voice(config=None):
    config = config or {}
    client = get_speech_client(config)
    response = client.describe_voices(LanguageCode=config.get("language_code", "en-US"))
    return response["Voices"]