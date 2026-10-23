import os
from google.cloud import speech_v1
from google.oauth2 import service_account


class SpeechClient:
    """Local configuration and client helper utilities for Batch Speech-to-Text."""

    def __init__(self, credentials_path=None):
        """Initialize Google Cloud Speech client with optional credentials."""
        if credentials_path and os.path.exists(credentials_path):
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
            self.client = speech_v1.SpeechClient(credentials=credentials)
        else:
            self.client = speech_v1.SpeechClient()

    def get_client(self):
        """Return the configured Speech client."""
        return self.client

    @staticmethod
    def get_supported_languages():
        """Return list of supported language codes."""
        return [
            "en-US",
            "en-GB",
            "es-ES",
            "fr-FR",
            "de-DE",
            "ja-JP",
            "ko-KR",
            "zh-CN",
            "zh-TW",
        ]

    @staticmethod
    def get_supported_models():
        """Return dictionary of supported models."""
        return {
            "default": "Best for most audio types",
            "video": "Optimized for video content",
            "phone_call": "Optimized for phone call audio",
            "command_and_search": "Optimized for short commands",
        }

    @staticmethod
    def validate_audio_file(file_path):
        """Validate audio file exists and has supported extension."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        supported_extensions = [".wav", ".flac", ".mp3", ".ogg", ".m4a"]
        if not any(file_path.lower().endswith(ext) for ext in supported_extensions):
            raise ValueError(
                f"Unsupported audio format. Supported: {supported_extensions}"
            )

        return True
