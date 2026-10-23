import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from speech_client import create_streaming_client

client = create_streaming_client()
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='en-US',
)
streaming_config = types.StreamingRecognitionConfig(config=config, interim_results=True)

def stream_chunks(audio_generator):
    requests = (types.StreamingRecognizeRequest(audio_content=content) for content in audio_generator())
    responses = client.streaming_recognize(streaming_config, requests)
    for response in responses:
        for result in response.results:
            print(result.alternatives[0].transcript)