from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from speech_client import create_streaming_client

client = create_streaming_client()

def handle_partial_results(responses):
    for response in responses:
        for result in response.results:
            if not result.is_final:
                print('Interim transcript: {}'.format(result.alternatives[0].transcript))
            else:
                print('Final transcript: {}'.format(result.alternatives[0].transcript))