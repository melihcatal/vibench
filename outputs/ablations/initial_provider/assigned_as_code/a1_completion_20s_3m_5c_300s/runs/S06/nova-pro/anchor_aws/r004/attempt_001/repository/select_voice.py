import boto3

from speech_client import get_polly_client


def select_voice(locale, config=None):
    config = config or {}
    client = get_polly_client(config)
    response = client.describe_voices(LanguageCode=locale)
    voices = response['Voices']
    return voices