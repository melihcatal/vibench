from speech_client import SpeechClient

def synthesize_ssml(api_key, endpoint, ssml):
    client = SpeechClient(api_key, endpoint)
    return client.synthesize_ssml(ssml)