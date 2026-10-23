import os
from google.cloud import texttospeech
from google.oauth2 import service_account


class SpeechClient:
    """Configuration and client helper utilities for Text-to-Speech."""

    def __init__(self, credentials_path=None, project_id=None):
        """Initialize TTS client with optional credentials."""
        self.credentials_path = credentials_path or os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self._client = None

    @property
    def client(self):
        """Lazy-loaded TTS client."""
        if self._client is None:
            if self.credentials_path and os.path.exists(self.credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
                self._client = texttospeech.TextToSpeechClient(credentials=credentials)
            else:
                self._client = texttospeech.TextToSpeechClient()
        return self._client

    def get_default_voice_params(self, language_code="en-US"):
        """Get default voice parameters for a language."""
        return texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )

    def get_default_audio_config(self, encoding="MP3"):
        """Get default audio configuration."""
        encoding_map = {
            "MP3": texttospeech.AudioEncoding.MP3,
            "LINEAR16": texttospeech.AudioEncoding.LINEAR16,
            "OGG_OPUS": texttospeech.AudioEncoding.OGG_OPUS,
        }

        return texttospeech.AudioConfig(
            audio_encoding=encoding_map.get(encoding, texttospeech.AudioEncoding.MP3)
        )

    def validate_text(self, text, max_length=5000):
        """Validate text length for synthesis."""
        if len(text) > max_length:
            raise ValueError(f"Text exceeds maximum length of {max_length} characters")
        return True
