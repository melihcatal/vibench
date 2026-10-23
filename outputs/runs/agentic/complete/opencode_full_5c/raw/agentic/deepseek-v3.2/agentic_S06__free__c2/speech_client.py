import os
from google.cloud import texttospeech
from google.oauth2 import service_account


def get_tts_client(credentials_path=None):
    """Get a configured Google Cloud Text-to-Speech client."""
    if credentials_path and os.path.exists(credentials_path):
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        client = texttospeech.TextToSpeechClient(credentials=credentials)
    else:
        client = texttospeech.TextToSpeechClient()

    return client


def get_default_voice_config():
    """Get default voice configuration."""
    return {
        "language_code": "en-US",
        "name": "en-US-Neural2-J",
        "ssml_gender": texttospeech.SsmlVoiceGender.NEUTRAL,
    }


def get_default_audio_config():
    """Get default audio configuration."""
    return {
        "audio_encoding": texttospeech.AudioEncoding.MP3,
        "speaking_rate": 1.0,
        "pitch": 0.0,
        "volume_gain_db": 0.0,
    }


def create_synthesis_input(text=None, ssml=None):
    """Create synthesis input from text or SSML."""
    if ssml:
        return texttospeech.SynthesisInput(ssml=ssml)
    elif text:
        return texttospeech.SynthesisInput(text=text)
    else:
        raise ValueError("Either text or ssml must be provided")


def validate_text_length(text, max_length=5000):
    """Validate text length for synthesis."""
    if len(text) > max_length:
        raise ValueError(f"Text exceeds maximum length of {max_length} characters")
    return True
