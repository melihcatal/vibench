from google.cloud import speech_v1p1beta1 as speech
import os
from typing import Optional, Dict, Any


class SpeechClient:
    """Provides local configuration and client helper utilities for Google Cloud Speech-to-Text."""

    def __init__(self, credentials_path: Optional[str] = None):
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.client = speech.SpeechClient()

    def get_client(self):
        """Returns the initialized Speech-to-Text client."""
        return self.client

    def create_recognition_config(
        self,
        language_code: str = "en-US",
        model: str = "latest_long",
        enable_punctuation: bool = True,
    ) -> speech.RecognitionConfig:
        """Creates a recognition config with the specified settings."""
        return speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=enable_punctuation,
            model=model,
        )

    def create_streaming_config(
        self, config: speech.RecognitionConfig, interim_results: bool = True
    ) -> speech.StreamingRecognitionConfig:
        """Creates a streaming recognition config."""
        return speech.StreamingRecognitionConfig(
            config=config, interim_results=interim_results
        )
