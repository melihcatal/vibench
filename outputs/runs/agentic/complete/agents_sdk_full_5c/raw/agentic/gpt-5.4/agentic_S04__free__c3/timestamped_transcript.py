from __future__ import annotations

from typing import Any, Dict, List, Optional

from speech_client import get_transcript


def timestamped_transcript(
    transcript_id: str,
    api_key: Optional[str] = None,
    granularity: str = "word",
) -> Dict[str, Any]:
    payload = get_transcript(transcript_id, api_key=api_key)
    if payload.get("status") != "completed":
        return {
            "provider": "AssemblyAI",
            "transcript_id": transcript_id,
            "status": payload.get("status"),
            "timestamps": [],
        }

    timestamps: List[Dict[str, Any]] = []
    if granularity == "segment":
        for item in payload.get("utterances") or []:
            timestamps.append(
                {
                    "text": item.get("text", ""),
                    "start_ms": item.get("start"),
                    "end_ms": item.get("end"),
                    "speaker": item.get("speaker"),
                }
            )
    else:
        for item in payload.get("words") or []:
            timestamps.append(
                {
                    "text": item.get("text", ""),
                    "start_ms": item.get("start"),
                    "end_ms": item.get("end"),
                    "confidence": item.get("confidence"),
                    "speaker": item.get("speaker"),
                }
            )

    return {
        "provider": "AssemblyAI",
        "transcript_id": transcript_id,
        "status": payload.get("status"),
        "granularity": granularity,
        "timestamps": timestamps,
    }
