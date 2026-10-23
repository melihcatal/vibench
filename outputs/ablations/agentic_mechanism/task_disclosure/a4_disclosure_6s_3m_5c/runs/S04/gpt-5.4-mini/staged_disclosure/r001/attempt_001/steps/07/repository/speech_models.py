from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

OPENAI_BATCH_TRANSCRIPTION_ENDPOINT = "/v1/audio/transcriptions"
OPENAI_BATCH_MODEL = "gpt-4o-mini-transcribe"


@dataclass(frozen=True)
class BatchSpeechRequest:
    audio_path: Path
    model: str = OPENAI_BATCH_MODEL
    response_format: str = "verbose_json"
    timestamp_granularities: List[str] = field(default_factory=lambda: ["word", "segment"])


@dataclass(frozen=True)
class BatchSpeechResponse:
    raw: Dict[str, Any]

    @property
    def text(self) -> str:
        return normalize_transcript_text(self.raw)

    @property
    def words(self) -> List[Dict[str, Any]]:
        return normalize_timestamps(self.raw).get("words", [])

    @property
    def segments(self) -> List[Dict[str, Any]]:
        return normalize_timestamps(self.raw).get("segments", [])


def normalize_transcript_text(payload: Dict[str, Any]) -> str:
    for key in ("text", "transcript"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    response = payload.get("response")
    if isinstance(response, dict):
        body = response.get("body")
        if isinstance(body, dict):
            for key in ("text", "transcript"):
                value = body.get(key)
                if isinstance(value, str) and value:
                    return value
    return ""


def normalize_timestamps(payload: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    words = payload.get("words")
    segments = payload.get("segments")
    normalized_words = list(words) if isinstance(words, Iterable) else []
    normalized_segments = list(segments) if isinstance(segments, Iterable) else []
    return {"words": normalized_words, "segments": normalized_segments}


def normalize_batch_speech_response(payload: Dict[str, Any]) -> BatchSpeechResponse:
    return BatchSpeechResponse(raw=payload)
