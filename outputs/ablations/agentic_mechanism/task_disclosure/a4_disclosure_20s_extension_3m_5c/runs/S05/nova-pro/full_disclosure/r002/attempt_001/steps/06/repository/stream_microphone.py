import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def stream_microphone():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = speech.SpeechClient()

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_automatic_punctuation=True)

    streaming_config = types.StreamingRecognitionConfig(config=config, interim_results=True)

    with io.BytesIO() as stream:
        while True:
            chunk = stream.read(1024)
            if not chunk:
                break
            audio = types.StreamingRecognizeRequest(audio_content=chunk)
            responses = client.streaming_recognize(streaming_config, [audio])
            for response in responses:
                for result in response.results:
                    print('Transcript: {}'.format(result.alternatives[0].transcript))

if __name__ == '__main__':
    stream_microphone()