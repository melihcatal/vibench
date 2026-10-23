import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from speech_client import create_speech_client
from speech_models import StreamingRecognizeRequest, StreamingRecognitionConfig


def stream_microphone():
    client = create_speech_client()
    config = StreamingRecognitionConfig(
        config=types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US'),
        interim_results=True)

    with MicrophoneStream(rate=16000) as stream:
        audio_generator = stream.generator()
        requests = (StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(config, requests)

        for response in responses:
            for result in response.results:
                print(u'Transcript: {}'.format(result.alternatives[0].transcript))

if __name__ == '__main__':
    stream_microphone()