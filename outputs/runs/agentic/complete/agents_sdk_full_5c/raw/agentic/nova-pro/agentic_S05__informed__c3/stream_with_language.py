from google.cloud import speech
from speech_client import get_speech_client
from speech_models import create_streaming_config, normalize_response

# Starts a streaming recognizer with language and punctuation settings

def stream_with_language(language_code='en-US'):
    client = get_speech_client()
    config = create_streaming_config(language_code)
    print('Listening in', language_code, 'with punctuation...')
    while True:
        # Placeholder for actual audio streaming logic
        pass