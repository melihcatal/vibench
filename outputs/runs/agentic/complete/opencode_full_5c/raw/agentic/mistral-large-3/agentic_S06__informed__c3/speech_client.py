import os
from google.cloud import texttospeech_v1 as texttospeech
from typing import Optional


class SpeechClient:
    """Provides local configuration and client helper utilities for Google Cloud Text-to-Speech."""

    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    @staticmethod
    def get_audio_encoding(encoding: str) -> int:
        """Converts a string audio encoding to the corresponding enum value."""
        return getattr(texttospeech.AudioEncoding, encoding)

    @staticmethod
    def get_ssml_gender(gender: str) -> int:
        """Converts a string SSML gender to the corresponding enum value."""
        return getattr(texttospeech.SsmlVoiceGender, gender)

    def get_client(self) -> texttospeech.TextToSpeechClient:
        """Returns the initialized Text-to-Speech client."""
        return self.client
