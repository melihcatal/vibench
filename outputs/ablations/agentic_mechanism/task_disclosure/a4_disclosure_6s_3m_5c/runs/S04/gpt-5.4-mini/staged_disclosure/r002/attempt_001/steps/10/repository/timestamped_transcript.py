from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from openai import OpenAI


@dataclass(frozen=True)
class TimestampedItem:
    start: float
    end: float
    text: str


def _normalize_timestamp_item(item: Dict[str, Any]) -> TimestampedItem:
    start = float(item.get("start", 0.0))
    end = float(item.get("end", 0.0))
    text = str(item.get("text", ""))
    return TimestampedItem(start=start, end=end, text=text)


def transcript_timestamps(
    audio_file: Any,
    *,
    model: str = "whisper-1",
    timestamp_granularities: Optional[List[str]] = None,
) -> Union[List[TimestampedItem], Dict[str, List[TimestampedItem]]]:
    client = OpenAI()
    response = client.audio.transcriptions.create(
        model=model,
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=timestamp_granularities or ["word"],
    )
    data = response.model_dump() if hasattr(response, "model_dump") else dict(response)
    words = data.get("words") or []
    segments = data.get("segments") or []
    result: Dict[str, List[TimestampedItem]] = {}
    if words:
        result["words"] = [_normalize_timestamp_item(item) for item in words]
    if segments:
        result["segments"] = [_normalize_timestamp_item(item) for item in segments]
    if len(result) == 1:
        return next(iter(result.values()))
    return result
