from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _pick(d: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in d and d[key] is not None:
            return d[key]
    return default


def _segments(items: Any) -> List[Dict[str, Any]]:
    return list(items) if isinstance(items, list) else []


@dataclass
class TranscriptionRequest:
    audio_url: Optional[str] = None
    audio_file: Optional[str] = None
    language_code: Optional[str] = None
    speaker_labels: bool = False
    timestamps: bool = False


@dataclass
class TranscriptionResult:
    id: str
    status: str
    text: str
    raw: Dict[str, Any]


def normalize_assemblyai_transcript(payload: Dict[str, Any]) -> TranscriptionResult:
    return TranscriptionResult(
        id=str(_pick(payload, "id", "utterance_id", default="")),
        status=str(_pick(payload, "status", default="unknown")),
        text=str(_pick(payload, "text", default="")),
        raw=payload,
    )


def extract_segments(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return _segments(_pick(payload, "utterances", "segments", "words", default=[]))


def extract_diarized_speakers(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    speakers = _pick(payload, "utterances", "speakers", default=[])
    return _segments(speakers)
