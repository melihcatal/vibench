from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from speech_client import create_streaming_client

client = create_streaming_client()
config = types.StreamingRecognitionConfig(config={
    'encoding': enums.RecognitionConfig.AudioEncoding.LINEAR16,
    'sample_rate_hertz': 16000,
    'language_code': 'en-US',
}, interim_results=True)

def handle_partial_results(responses):
    for response in responses:
        for result in response.results:
            if not result.is_final:
                yield result.alternatives[0].transcript
            else:
                yield result.alternatives[0].transcript