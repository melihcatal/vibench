from google.cloud import speech_v1p1beta1 as speech
from google.api_core.client_options import ClientOptions
import os
from typing import Optional


class SpeechClient:
    """Provides local configuration and client helper utilities for Streaming Speech-to-Text."""

    def __init__(self, api_key: Optional[str] = None, region: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.region = region or os.getenv("GOOGLE_REGION", "us-central1")
        self.client_options = ClientOptions(
            api_key=self.api_key,
            quota_project_id=os.getenv("GOOGLE_PROJECT_ID"),
        )
        self.client = speech.SpeechClient(client_options=self.client_options)

    def get_client(self) -> speech.SpeechClient:
        """Returns the configured Speech-to-Text client."""
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
            model=model,
            enable_automatic_punctuation=enable_punctuation,
        )
