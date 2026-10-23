from __future__ import annotations

from typing import Any, Dict, List, Optional

from speech_client import AssemblyAIBatchSpeechClient


def timestamped_transcript(
    transcript_id: str, granularity: str = "word"
) -> Dict[str, Any]:
    client = AssemblyAIBatchSpeechClient()
    job = client.get_transcription(transcript_id)
    if granularity == "segment":
        items: List[Dict[str, Any]] = [
            {
                "text": item.text,
                "start_ms": item.start_ms,
                "end_ms": item.end_ms,
                "speaker": item.speaker,
                "confidence": item.confidence,
            }
            for item in job.utterances
        ]
    else:
        items = [
            {
                "text": item.text,
                "start_ms": item.start_ms,
                "end_ms": item.end_ms,
                "confidence": item.confidence,
                "speaker": item.metadata.get("speaker"),
            }
            for item in job.words
        ]
    return {
        "provider": "AssemblyAI",
        "transcript_id": job.transcript_id,
        "status": job.status,
        "granularity": granularity,
        "timestamps": items,
    }
