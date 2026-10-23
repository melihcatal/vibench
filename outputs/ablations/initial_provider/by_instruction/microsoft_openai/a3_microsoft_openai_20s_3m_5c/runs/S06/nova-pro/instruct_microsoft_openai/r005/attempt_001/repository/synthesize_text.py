from speech_client import SpeechClient

def synthesize_text(api_key, endpoint, text):
    client = SpeechClient(api_key, endpoint)
    return client.synthesize_text(text)