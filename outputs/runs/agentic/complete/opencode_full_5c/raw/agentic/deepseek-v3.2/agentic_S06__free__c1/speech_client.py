import os
from google.cloud import texttospeech
from google.oauth2 import service_account


def get_tts_client(credentials_path=None):
    """Get a configured Text-to-Speech client."""
    if credentials_path and os.path.exists(credentials_path):
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        client = texttospeech.TextToSpeechClient(credentials=credentials)
    else:
        client = texttospeech.TextToSpeechClient()

    return client


def get_default_audio_config():
    """Get default audio configuration."""
    from google.cloud import texttospeech

    return texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0,
        pitch=0.0,
        volume_gain_db=0.0,
    )


def validate_text_length(text, max_chars=5000):
    """Validate text length for synthesis."""
    if len(text) > max_chars:
        raise ValueError(f"Text exceeds maximum length of {max_chars} characters")
    return True
