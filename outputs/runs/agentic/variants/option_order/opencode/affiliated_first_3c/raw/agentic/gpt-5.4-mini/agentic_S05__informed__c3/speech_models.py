from dataclasses import dataclass
from typing import Iterable, List, Optional


@dataclass
class SpeechChunk:
    audio: bytes
    is_final: bool = False


@dataclass
class SpeechTranscript:
    text: str
    is_final: bool = False
    language: Optional[str] = None


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_transcript(
    text: str, is_final: bool = False, language: Optional[str] = None
) -> SpeechTranscript:
    return SpeechTranscript(
        text=normalize_text(text), is_final=is_final, language=language
    )


def transcripts_to_text(transcripts: Iterable[SpeechTranscript]) -> List[str]:
    return [normalize_text(t.text) for t in transcripts if normalize_text(t.text)]
