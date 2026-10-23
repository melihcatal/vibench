from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class TranscriptionJobRequest:
    audio_path: str
    model: str = "gpt-4o-mini-transcribe"
    language: Optional[str] = None
    prompt: Optional[str] = None
    response_format: str = "json"


@dataclass
class TranscriptionJobStatus:
    id: str
    status: Optional[str] = None
    text: Optional[str] = None


def normalize_transcription_result(result: Any) -> Dict[str, Any]:
    if hasattr(result, "model_dump"):
        return result.model_dump()
    if hasattr(result, "dict"):
        return result.dict()
    if isinstance(result, dict):
        return result
    return {"text": getattr(result, "text", None), "raw": str(result)}
