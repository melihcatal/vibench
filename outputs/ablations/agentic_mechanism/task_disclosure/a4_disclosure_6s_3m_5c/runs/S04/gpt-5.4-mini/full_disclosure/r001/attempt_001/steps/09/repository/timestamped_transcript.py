import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _normalize_items(items: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    if not items:
        return normalized
    for item in items:
        start = item.get("start")
        end = item.get("end")
        text = item.get("text") or item.get("word") or item.get("segment")
        entry: Dict[str, Any] = {"text": text}
        if start is not None:
            entry["start"] = start
        if end is not None:
            entry["end"] = end
        if "speaker" in item:
            entry["speaker"] = item["speaker"]
        normalized.append(entry)
    return normalized


def timestamped_transcript(transcription: Dict[str, Any], granularity: str = "segment") -> Dict[str, Any]:
    if granularity not in {"word", "segment"}:
        raise ValueError("granularity must be 'word' or 'segment'")
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    _ = client
    timestamps_key = "words" if granularity == "word" else "segments"
    return {
        "transcript": transcription.get("text") or transcription.get("transcript") or "",
        "timestamps": _normalize_items(transcription.get(timestamps_key)),
        "provider": "openai",
        "model": transcription.get("model") or "gpt-4o-transcribe",
    }
