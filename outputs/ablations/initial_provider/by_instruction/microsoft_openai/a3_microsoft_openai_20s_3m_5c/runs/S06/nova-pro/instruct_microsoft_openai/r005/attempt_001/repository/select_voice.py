from speech_client import SpeechClient

def select_voice(api_key, endpoint):
    client = SpeechClient(api_key, endpoint)
    return client.list_voices()