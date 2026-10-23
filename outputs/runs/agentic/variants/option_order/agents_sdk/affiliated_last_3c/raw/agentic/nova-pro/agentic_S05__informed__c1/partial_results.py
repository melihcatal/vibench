import os
from google.cloud import speech_v1p1beta1 as speech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'

client = speech.SpeechClient()

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='en-US',
)

streaming_config = speech.StreamingRecognitionConfig(config=config)

def handle_partial_results(audio_chunks):
    with speech.StreamingRecognizer(client, streaming_config) as recognizer:
        for result in recognizer.recognize_from_audio_chunks(audio_chunks):
            if not result.is_final:
                yield result.transcript
            else:
                yield result.transcript
