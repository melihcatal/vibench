import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

client = speech.SpeechClient()

def stream_microphone():
    audio = io.BytesIO()
    with speech.SpeechClient() as client:
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US',
            max_alternatives=1,
            enable_automatic_punctuation=True,
            interim_results=True)

        streaming_config = types.StreamingRecognitionConfig(config=config)

        with client.streaming_recognize(streaming_config) as stream:
            while True:
                chunk = audio.read(1024)
                if not chunk:
                    break
                audio.write(chunk)
                stream.send_audio(chunk)
                response = stream.next()
                for result in response.results:
                    yield result.alternatives[0].transcript

if __name__ == '__main__':
    for transcript in stream_microphone():
        print(transcript)