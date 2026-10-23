import os
from google.cloud import speech_v1


def get_speech_client():
    """Get Google Cloud Speech-to-Text client with configuration."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    return speech_v1.SpeechClient()


def validate_audio_file(audio_file_path):
    """Validate audio file exists and is readable."""
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    if not os.access(audio_file_path, os.R_OK):
        raise PermissionError(f"Cannot read audio file: {audio_file_path}")

    return True


def get_supported_languages():
    """Return list of supported language codes for Google Cloud Speech-to-Text."""
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
