import os
from google.cloud import texttospeech
from google.cloud import storage
from google.oauth2 import service_account


def get_tts_client(credentials_path=None):
    """Get a Text-to-Speech client with optional credentials."""
    if credentials_path and os.path.exists(credentials_path):
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        return texttospeech.TextToSpeechClient(credentials=credentials)
    else:
        return texttospeech.TextToSpeechClient()


def get_storage_client(credentials_path=None):
    """Get a Cloud Storage client with optional credentials."""
    if credentials_path and os.path.exists(credentials_path):
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        return storage.Client(credentials=credentials)
    else:
        return storage.Client()


def get_default_voice_params(language_code="en-US", voice_name=None):
    """Get default voice parameters for a given language."""
    from google.cloud import texttospeech

    if voice_name:
        return texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )
    else:
        return texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=f"{language_code}-Standard-A",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )


def get_default_audio_config(audio_encoding="MP3"):
    """Get default audio configuration."""
    from google.cloud import texttospeech

    encoding_map = {
        "MP3": texttospeech.AudioEncoding.MP3,
        "LINEAR16": texttospeech.AudioEncoding.LINEAR16,
        "OGG_OPUS": texttospeech.AudioEncoding.OGG_OPUS,
    }

    return texttospeech.AudioConfig(
        audio_encoding=encoding_map.get(audio_encoding, texttospeech.AudioEncoding.MP3)
    )
