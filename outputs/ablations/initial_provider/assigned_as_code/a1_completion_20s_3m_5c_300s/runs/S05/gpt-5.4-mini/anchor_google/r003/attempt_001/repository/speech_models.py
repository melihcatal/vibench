from dataclasses import dataclass


def normalize_transcript(text):
    return " ".join(str(text).split())


@dataclass
class SpeechStreamPayload:
    sample_rate_hz: int
    language_code: str
    audio_chunks: list


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool


@dataclass
class CaptionRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class SafetyRequest:
    text: str


@dataclass
class SummaryRequest:
    transcript_chunks: list


@dataclass
class EmbeddingRequest:
    text: str
