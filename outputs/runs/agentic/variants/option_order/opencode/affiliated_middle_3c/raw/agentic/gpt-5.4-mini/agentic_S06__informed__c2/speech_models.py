from dataclasses import dataclass


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


@dataclass
class SynthesisRequest:
    text: str
    voice_id: str | None = None
    model_id: str = "eleven_multilingual_v2"


@dataclass
class SynthesisResult:
    audio: bytes
    content_type: str = "audio/mpeg"


def ssml_wrap(text: str) -> str:
    return f"<speak>{text}</speak>"
