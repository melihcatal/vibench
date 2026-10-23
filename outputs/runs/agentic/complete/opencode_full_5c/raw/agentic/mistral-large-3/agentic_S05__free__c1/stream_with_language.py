from google.cloud import speech_v1p1beta1 as speech
from typing import Optional


class StreamingRecognizer:
    """Starts a streaming recognizer with language and punctuation settings."""

    def __init__(
        self,
        language_code: str = "en-US",
        model: str = "latest_long",
        enable_punctuation: bool = True,
    ):
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=enable_punctuation,
            model=model,
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config, interim_results=True
        )

    def recognize(self, audio_generator):
        """Starts streaming recognition on the provided audio generator."""
        requests = (
            speech.StreamingRecognizeRequest(audio_content=chunk)
            for chunk in audio_generator
        )
        responses = self.client.streaming_recognize(self.streaming_config, requests)
        return responses
