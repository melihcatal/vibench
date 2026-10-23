from dataclasses import dataclass


def normalize_text(text):
    return " ".join(str(text).split()).strip()


@dataclass
class StreamingAudioPayload:
    language_code: str
    sample_rate_hz: int
    audio_chunks: object


@dataclass
class CaptionChunk:
    text: str
    is_final: bool = False


@dataclass
class TranslationResult:
    text: str
    target_language: str


@dataclass
class SafetyResult:
    text: str
    unsafe: bool


@dataclass
class SummaryResult:
    text: str


@dataclass
class EmbeddingResult:
    text: str
    vector: object
