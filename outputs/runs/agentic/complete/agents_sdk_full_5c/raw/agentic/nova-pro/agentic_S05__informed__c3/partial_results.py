from google.cloud import speech
from speech_client import get_speech_client
from speech_models import create_streaming_config, normalize_response

# Handles partial and final streaming recognition events

def handle_partial_results(response):
    client = get_speech_client()
    for result in response.results:
        if not result.is_final:
            print('Interim transcript:', result.alternatives[0].transcript)
        else:
            print('Final transcript:', result.alternatives[0].transcript)