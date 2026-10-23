import os
from google.cloud import texttospeech

_tts_client = None


def get_tts_client():
    """
    Provide local configuration and client helper utilities for Google Cloud Text-to-Speech.
    """
    global _tts_client

    if _tts_client is None:
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        if credentials_path and os.path.exists(credentials_path):
            _tts_client = texttospeech.TextToSpeechClient.from_service_account_json(
                credentials_path
            )
        else:
            _tts_client = texttospeech.TextToSpeechClient()

    return _tts_client


def validate_voice_params(voice_id: str, language_code: str) -> tuple:
    """
    Validate and normalize voice parameters.
    """
    if not voice_id:
        if language_code.startswith("en"):
            voice_id = "en-US-Neural2-J"
        elif language_code.startswith("es"):
            voice_id = "es-US-Neural2-A"
        elif language_code.startswith("fr"):
            voice_id = "fr-FR-Neural2-A"
        else:
            voice_id = "en-US-Neural2-J"

    return voice_id, language_code


def get_default_audio_config():
    """
    Get default audio configuration.
    """
    return {
        "audio_encoding": "MP3",
        "speaking_rate": 1.0,
        "pitch": 0.0,
        "volume_gain_db": 0.0,
    }
