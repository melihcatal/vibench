import os
from google.cloud import speech
from speech_client import create_speech_client
from speech_models import StreamingRecognizeRequest, StreamingRecognitionConfig


def stream_with_language():
    client = create_speech_client()
    config = StreamingRecognitionConfig(
        config=speech.types.RecognitionConfig(
            encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US',
            enable_automatic_punctuation=True),
        interim_results=True)

    with MicrophoneStream(rate=16000) as stream:
        audio_generator = stream.generator()
        requests = (StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(config, requests)

        for response in responses:
            handle_partial_results(response)

if __name__ == '__main__':
    stream_with_language()