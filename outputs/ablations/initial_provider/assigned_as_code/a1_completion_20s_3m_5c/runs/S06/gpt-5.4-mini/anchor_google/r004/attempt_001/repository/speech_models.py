from dataclasses import dataclass


def normalize_locale(locale):
    return (locale or "en-US").replace("_", "-")


@dataclass
class TTSRequest:
    text: str
    locale: str = "en-US"
    voice_name: str | None = None


@dataclass
class TTSResponse:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
