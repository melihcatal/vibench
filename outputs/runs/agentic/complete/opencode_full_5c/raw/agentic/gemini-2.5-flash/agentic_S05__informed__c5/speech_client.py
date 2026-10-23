import os
from google.cloud import speech


class SpeechClientHelper:
    def __init__(self):
        self.client = speech.SpeechClient()

    def get_streaming_config(
        self, language_code="en-US", enable_automatic_punctuation=True
    ):
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=enable_automatic_punctuation,
        )
        return speech.StreamingRecognitionConfig(config=config, interim_results=True)

    def streaming_recognize(self, requests, streaming_config):
        return self.client.streaming_recognize(streaming_config, requests)
