import os
from google.cloud import speech_v1p1beta1 as speech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'

client = speech.SpeechClient()

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='en-US',
    enable_automatic_punctuation=True,
)

streaming_config = speech.StreamingRecognitionConfig(config=config)

def stream_with_language():
    with speech.StreamingRecognizer(client, streaming_config) as recognizer:
        for result in recognizer.recognize_from_microphone():
            yield result.transcript
