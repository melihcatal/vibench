from __future__ import annotations

from typing import Any, Dict, List, Literal

from speech_client import get_speech_client
from speech_models import normalize_transcript_response



def timestamped_transcript(transcript_id: str, level: Literal["word", "segment"] = "word") -> Dict[str, Any]:
    client = get_speech_client()
    data = client.get(f"transcript/{transcript_id}")
    result = normalize_transcript_response(data)
    if level == "segment":
        items: List[Dict[str, Any]] = [
            {
                "text": u.text,
                "start_ms": u.start_ms,
                "end_ms": u.end_ms,
                "speaker": u.speaker,
            }
            for u in result.utterances
        ]
    else:
        items = [
            {
                "text": w.text,
                "start_ms": w.start_ms,
                "end_ms": w.end_ms,
                "confidence": w.confidence,
            }
            for w in result.words
        ]
    return {
        "provider": "AssemblyAI",
        "transcript_id": result.transcript_id,
        "status": result.status,
        "level": level,
        "timestamps": items,
    }
