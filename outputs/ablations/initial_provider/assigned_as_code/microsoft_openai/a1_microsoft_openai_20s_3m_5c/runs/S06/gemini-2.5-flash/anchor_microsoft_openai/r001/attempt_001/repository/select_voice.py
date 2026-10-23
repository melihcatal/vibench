from speech_client import AzureSpeechClient
import os

def select_voice(locale=None, config=None):
    config = config or {}
    subscription_key = config.get('api_key', os.environ.get('AZURE_SPEECH_KEY'))
    region = config.get('region', os.environ.get('AZURE_SPEECH_REGION'))

    client = AzureSpeechClient(subscription_key, region)
    available_voices = client.list_voices()

    if locale:
        filtered_voices = [voice for voice in available_voices if voice['locale'].lower() == locale.lower()]
        return filtered_voices
    else:
        return available_voices