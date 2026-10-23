import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from speech_client import create_streaming_client

client = create_streaming_client()

def stream_with_language():
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_automatic_punctuation=True,
    )
    streaming_config = types.StreamingRecognitionConfig(config=config, interim_results=True)

    with client:
        for request in client.streaming_recognize(streaming_config):
            if request.results:
                for result in request.results:
                    print('Transcript: {}'.format(result.alternatives[0].transcript))
                    if result.is_final:
                        print('Final transcript: {}'.format(result.alternatives[0].transcript))