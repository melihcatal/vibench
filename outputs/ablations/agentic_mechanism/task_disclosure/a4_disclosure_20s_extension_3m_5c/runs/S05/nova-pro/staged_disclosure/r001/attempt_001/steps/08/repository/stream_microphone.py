import io
import os

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types


def stream_microphone():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'

    client = speech.SpeechClient()

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_automatic_punctuation=True,
    )

    streaming_config = types.StreamingRecognitionConfig(config=config, interim_results=True)

    with io.BytesIO() as audio_file:
        print('Start speaking. Press Ctrl+C to stop.')
        try:
            while True:
                chunk = audio_file.read(1024)
                if not chunk:
                    break
                audio = types.StreamingRecognizeRequest(audio_content=chunk)
                responses = client.streaming_recognize(streaming_config, [audio])
                for response in responses:
                    for result in response.results:
                        print('Transcript: {}'.format(result.alternatives[0].transcript))
        except KeyboardInterrupt:
            pass

    print('Streaming stopped.')


if __name__ == '__main__':
    stream_microphone()