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
    enable_automatic_punctuation=True,
)
streaming_config = types.StreamingRecognitionConfig(config=config, interim_results=True)

def start_streaming_with_language():
    import pyaudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()
    requests = (types.StreamingRecognizeRequest(audio_content=content) for content in iter(lambda: stream.read(1024), ''))
    responses = client.streaming_recognize(streaming_config, requests)
    for response in responses:
        for result in response.results:
            print(result.alternatives[0].transcript)