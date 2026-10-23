from typing import Dict, Any, Optional
from google.cloud.speech_v1p1beta1 import types


class StreamingRecognitionConfig:
    """Defines local request and normalization helpers for Google Cloud Speech-to-Text."""

    def __init__(
        self,
        language_code: str = "en-US",
        interim_results: bool = True,
        enable_automatic_punctuation: bool = True,
    ):
        self.language_code = language_code
        self.interim_results = interim_results
        self.enable_automatic_punctuation = enable_automatic_punctuation

    def to_google_config(self) -> types.StreamingRecognitionConfig:
        """Converts the config to a Google Cloud Speech-to-Text streaming config."""
        return types.StreamingRecognitionConfig(
            config=types.RecognitionConfig(
                encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=self.language_code,
                enable_automatic_punctuation=self.enable_automatic_punctuation,
                model="latest_long",
            ),
            interim_results=self.interim_results,
        )
