from dataclasses import dataclass


@dataclass
class TextToSpeechRequest:
    text: str
    voice: str | None = None
    locale: str | None = None


@dataclass
class SsmlRequest:
    ssml: str
    voice: str | None = None
    locale: str | None = None


@dataclass
class VoiceInfo:
    name: str
    locale: str | None = None
    gender: str | None = None


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def wrap_ssml(
    text: str, voice: str, locale: str = "en-US", rate: str = "0%", pitch: str = "0%"
) -> str:
    return f'<speak version="1.0" xml:lang="{locale}"><voice name="{voice}"><prosody rate="{rate}" pitch="{pitch}">{text}</prosody></voice></speak>'
