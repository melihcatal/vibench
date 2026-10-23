import os
from typing import Optional
from google.cloud import texttospeech
from google.oauth2 import service_account


def get_tts_client(
    credentials_path: Optional[str] = None,
) -> texttospeech.TextToSpeechClient:
    """Provide local configuration and client helper utilities for Text-to-Speech."""
    if credentials_path and os.path.exists(credentials_path):
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        client = texttospeech.TextToSpeechClient(credentials=credentials)
    else:
        client = texttospeech.TextToSpeechClient()

    return client


def get_default_voice_config() -> dict:
    """Get default voice configuration."""
    return {
        "language_code": "en-US",
        "voice_name": "en-US-Neural2-F",
        "audio_encoding": "MP3",
    }


def validate_text_length(text: str, max_length: int = 5000) -> bool:
    """Validate text length for synthesis."""
    return len(text) <= max_length


def get_supported_audio_formats() -> list:
    """Get list of supported audio formats."""
    return ["MP3", "LINEAR16", "OGG_OPUS", "MULAW", "ALAW"]
