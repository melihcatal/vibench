import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def get_timestamped_transcript(result: Dict[str, Any], granularity: str = "segment") -> List[Dict[str, Any]]:
    if granularity not in {"segment", "word"}:
        raise ValueError("granularity must be 'segment' or 'word'")
    if granularity == "word":
        items = result.get("words") or result.get("segments") or []
    else:
        items = result.get("segments") or []
    normalized: List[Dict[str, Any]] = []
    for item in items:
        normalized.append(
            {
                "start": item.get("start"),
                "end": item.get("end"),
                "text": item.get("text") or item.get("word") or "",
                "speaker": item.get("speaker"),
            }
        )
    return normalized


class TimestampedTranscriptClient:
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

    def from_transcription_result(self, result: Dict[str, Any], granularity: str = "segment") -> List[Dict[str, Any]]:
        return get_timestamped_transcript(result, granularity=granularity)
