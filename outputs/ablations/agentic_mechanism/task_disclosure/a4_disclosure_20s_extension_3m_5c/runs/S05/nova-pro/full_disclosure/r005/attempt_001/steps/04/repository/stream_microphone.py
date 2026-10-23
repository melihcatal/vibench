import os
import io
import time
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Set environment variables
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'

def stream_microphone():
    client = speech.SpeechClient()

    def callback(response):
        print('Transcript: {}'.format(response.results[-1].alternatives[0].transcript))

    audio_config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        max_alternatives=1,
        enable_automatic_punctuation=True)

    streaming_config = types.StreamingRecognitionConfig(
        config=audio_config,
        interim_results=True)

    with io.BytesIO() as stream:
        stream.write(b'\xff\xf0')
        stream.seek(0)

        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in stream)

        responses = client.streaming_recognize(streaming_config, requests)

        for response in responses:
            callback(response)
            time.sleep(1)

if __name__ == '__main__':
    stream_microphone()