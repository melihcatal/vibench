from dataclasses import dataclass


def normalize_text(value):
    return " ".join(str(value).split())


def normalize_locale(value):
    return normalize_text(value).replace("_", "-").lower()


@dataclass
class SpeechRequest:
    text: str
    voice: str = "alloy"
    format: str = "mp3"


@dataclass
class SpeechResponse:
    audio: bytes
    voice: str
    format: str


@dataclass
class VoiceSelection:
    name: str
    locale: str
    description: str = ""
