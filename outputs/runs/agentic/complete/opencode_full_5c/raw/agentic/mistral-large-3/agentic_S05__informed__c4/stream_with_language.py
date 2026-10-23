import os
from typing import Optional

from speech_client import SpeechClient
from speech_models import SpeechEvent, SpeechNormalizer


class LanguageStreamRecognizer:
    """Starts a streaming recognizer with language and punctuation settings using DashScope."""

    def __init__(self, language: Optional[str] = None):
        self.client = SpeechClient()
        self.normalizer = SpeechNormalizer()
        self.language = language or os.getenv("STT_LANGUAGE", "en")

    def get_recognizer(self):
        """Initialize DashScope recognizer with language and punctuation settings."""
        return self.client.get_recognition_config(
            model="paraformer-realtime-v1",
            enable_punctuation_prediction=True,
            enable_inverse_text_normalization=True,
        )

    async def recognize(self, audio_source) -> SpeechEvent:
        """Recognize audio from source and return normalized event."""
        recognizer = self.get_recognizer()
        result = recognizer.call(audio_source)
        return self.normalizer.normalize_result(result)
