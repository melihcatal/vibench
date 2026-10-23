from dataclasses import dataclass


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_ssml(ssml: str) -> str:
    return ssml.strip()


@dataclass(frozen=True)
class SynthesisRequest:
    text: str
    language_code: str = "en-US"
    voice_name: str | None = None
    speaking_rate: float = 1.0
    pitch: float = 0.0


@dataclass(frozen=True)
class SynthesisResponse:
    audio_content: bytes
    content_type: str = "audio/mpeg"
