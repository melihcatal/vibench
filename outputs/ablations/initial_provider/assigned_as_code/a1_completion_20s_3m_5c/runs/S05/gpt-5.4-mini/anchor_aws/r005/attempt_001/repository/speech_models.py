from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def normalize_text(text: Optional[str]) -> str:
    return " ".join((text or "").strip().split())


def normalize_language(language: Optional[str]) -> str:
    return (language or "en-US").strip()


def normalize_punctuation(enabled: Optional[bool]) -> bool:
    return bool(True if enabled is None else enabled)


def normalize_chunks(chunks: Iterable[bytes]) -> List[bytes]:
    return [chunk for chunk in chunks if chunk]


@dataclass
class StreamingSpeechRequest:
    audio_chunks: List[bytes]
    language_code: str = "en-US"
    sample_rate_hz: int = 16000
    enable_punctuation: bool = True

    def normalized(self) -> Dict[str, Any]:
        return {
            "audio_chunks": normalize_chunks(self.audio_chunks),
            "language_code": normalize_language(self.language_code),
            "sample_rate_hz": int(self.sample_rate_hz),
            "enable_punctuation": normalize_punctuation(self.enable_punctuation),
        }


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool = False

    def as_dict(self) -> Dict[str, Any]:
        return {"text": normalize_text(self.text), "is_final": bool(self.is_final)}


@dataclass
class CaptionChunk:
    text: str
    language_code: str = "en-US"
    is_final: bool = False

    def as_dict(self) -> Dict[str, Any]:
        return {
            "text": normalize_text(self.text),
            "language_code": normalize_language(self.language_code),
            "is_final": bool(self.is_final),
        }
