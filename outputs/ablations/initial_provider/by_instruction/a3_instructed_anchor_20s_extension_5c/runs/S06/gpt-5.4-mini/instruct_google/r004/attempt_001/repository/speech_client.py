import os
from dataclasses import dataclass


@dataclass(frozen=True)
class SpeechConfig:
    google_application_credentials: str | None = None
    default_language_code: str = "en-US"
    default_voice_name: str | None = None
    default_speaking_rate: float = 1.0
    default_pitch: float = 0.0


def load_config() -> SpeechConfig:
    return SpeechConfig(
        google_application_credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        default_language_code=os.getenv("TTS_DEFAULT_LANGUAGE_CODE", "en-US"),
        default_voice_name=os.getenv("TTS_DEFAULT_VOICE_NAME"),
        default_speaking_rate=float(os.getenv("TTS_DEFAULT_SPEAKING_RATE", "1.0")),
        default_pitch=float(os.getenv("TTS_DEFAULT_PITCH", "0.0")),
    )


def build_client():
    from google.cloud import texttospeech

    return texttospeech.TextToSpeechClient()


def build_speech_settings(voice_name: str | None = None, language_code: str | None = None):
    cfg = load_config()
    from google.cloud import texttospeech

    return texttospeech.VoiceSelectionParams(
        language_code=language_code or cfg.default_language_code,
        name=voice_name or cfg.default_voice_name or "",
    )
