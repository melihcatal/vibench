from __future__ import annotations

from typing import Any, Dict, List

from speech_client import build_transcriber


def timestamped_transcript(job_id: str, level: str = "word") -> Dict[str, Any]:
    transcriber = build_transcriber()
    transcript = transcriber.get_by_id(job_id)
    if level == "segment":
        segments: List[Dict[str, Any]] = []
        for utterance in getattr(transcript, "utterances", None) or []:
            segments.append(
                {
                    "speaker": getattr(utterance, "speaker", None),
                    "text": getattr(utterance, "text", "") or "",
                    "start_ms": getattr(utterance, "start", None),
                    "end_ms": getattr(utterance, "end", None),
                }
            )
        return {
            "provider": "AssemblyAI",
            "job_id": getattr(transcript, "id", job_id),
            "status": getattr(transcript, "status", "unknown"),
            "timestamps": segments,
        }
    words = []
    for word in getattr(transcript, "words", None) or []:
        words.append(
            {
                "text": getattr(word, "text", "") or "",
                "start_ms": getattr(word, "start", None),
                "end_ms": getattr(word, "end", None),
                "confidence": getattr(word, "confidence", None),
                "speaker": getattr(word, "speaker", None),
            }
        )
    return {
        "provider": "AssemblyAI",
        "job_id": getattr(transcript, "id", job_id),
        "status": getattr(transcript, "status", "unknown"),
        "timestamps": words,
    }
