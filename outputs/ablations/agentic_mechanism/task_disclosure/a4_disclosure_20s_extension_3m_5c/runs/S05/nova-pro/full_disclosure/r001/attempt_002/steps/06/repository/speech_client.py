from google.cloud import speech_v1p1beta1 as speech

def create_client():
    config = {
        'encoding': 'LINEAR16',
        'sample_rate_hertz': 16000,
        'language_code': 'en-US',
    }
    client = speech.SpeechClient()
    return client, config

def authenticate_client():
    from google.auth import default
    credentials, project = default()
    return credentials, project