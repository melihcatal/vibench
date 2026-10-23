from google.cloud import speech_v1p1beta1 as speech
from typing import Optional


class StreamingRecognizer:
    """Starts a streaming recognizer with language and punctuation settings."""

    def __init__(
        self,
        language_code: str = "en-US",
        model: str = "latest_long",
        enable_punctuation: bool = True,
        enable_spoken_punctuation: bool = False,
        enable_spoken_emojis: bool = False,
    ):
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            model=model,
            enable_automatic_punctuation=enable_punctuation,
            enable_spoken_punctuation=enable_spoken_punctuation,
            enable_spoken_emojis=enable_spoken_emojis,
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config, interim_results=True
        )

    def start_stream(self):
        """Starts a streaming recognition session."""

        def request_generator():
            while True:
                yield None  # Placeholder for audio chunks

        responses = self.client.streaming_recognize(
            self.streaming_config, request_generator()
        )
        return responses
