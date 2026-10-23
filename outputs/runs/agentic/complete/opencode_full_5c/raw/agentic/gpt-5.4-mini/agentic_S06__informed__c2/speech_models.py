from dataclasses import dataclass


@dataclass
class TextToSpeechRequest:
    text: str
    locale: str = "en-US"
    voice: str | None = None


@dataclass
class SynthesisResult:
    audio: bytes
    voice: str | None = None
    locale: str | None = None


def normalize_text(text: str) -> str:
    return " ".join((text or "").split())


def normalize_ssml(text: str, voice: str, locale: str) -> str:
    content = normalize_text(text)
    return f'<speak version="1.0" xml:lang="{locale}"><voice name="{voice}">{content}</voice></speak>'
