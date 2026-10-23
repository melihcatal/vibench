from dataclasses import dataclass


@dataclass
class VoiceInfo:
    id: str
    locale: str
    gender: str
    description: str


@dataclass
class AudioOutput:
    file_path: str
    size_bytes: int
    content_type: str
    provider: str


@dataclass
class TtsRequest:
    text: str
    model: str
    voice: str
    response_format: str
    speed: float


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class SafetyResult:
    is_safe: bool
    flagged_categories: list[str]
    details: dict


@dataclass
class EmbeddingResult:
    text: str
    vector: list[float]
    model: str
    dimensions: int


@dataclass
class TranscriptResult:
    text: str
    language: str
    confidence: float
    segments: list[dict]


def normalize_ssml_request(
    ssml: str,
    model: str,
    voice: str,
    response_format: str,
    speed: float,
) -> dict:
    return {
        "model": model,
        "voice": voice,
        "input": ssml,
        "response_format": response_format,
        "speed": speed,
    }


def normalize_tts_request(
    text: str,
    model: str = "tts-1",
    voice: str = "alloy",
    response_format: str = "mp3",
    speed: float = 1.0,
) -> dict:
    return {
        "model": model,
        "voice": voice,
        "input": text,
        "response_format": response_format,
        "speed": speed,
    }
