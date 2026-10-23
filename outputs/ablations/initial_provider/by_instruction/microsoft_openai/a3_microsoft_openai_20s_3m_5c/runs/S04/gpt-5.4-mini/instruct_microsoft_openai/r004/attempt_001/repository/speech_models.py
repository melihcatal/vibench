from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionRequest:
    file_path: str
    model: str
    language: Optional[str] = None
    prompt: Optional[str] = None
    timestamp_granularities: Optional[List[str]] = None
    speaker_diarization: bool = False

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return {k: v for k, v in data.items() if v is not None}


def normalize_result(result: Dict[str, Any]) -> Dict[str, Any]:
    text = result.get("text") or result.get("transcript") or ""
    segments = result.get("segments") or []
    words = result.get("words") or []
    speakers = result.get("speaker_labels") or result.get("speaker_diarization") or []
    return {"text": text, "segments": segments, "words": words, "speakers": speakers, "raw": result}
