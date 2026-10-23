from __future__ import annotations

from typing import Literal

from speech_client import AssemblyAIClient, ensure_completed


def timestamped_transcript(transcript_id: str, granularity: Literal["word", "segment"] = "word") -> dict:
    client = AssemblyAIClient()
    result = ensure_completed(client.get_transcription(transcript_id))
    if granularity == "segment":
        segments = [
            {
                "text": item.text,
                "start_ms": item.start_ms,
                "end_ms": item.end_ms,
                "speaker": item.speaker,
            }
            for item in result.utterances
        ]
        if not segments and result.text:
            segments = [{"text": result.text, "start_ms": 0, "end_ms": result.audio_duration_ms, "speaker": None}]
        return {
            "provider": "AssemblyAI",
            "transcript_id": result.transcript_id,
            "granularity": "segment",
            "segments": segments,
        }
    words = [
        {
            "text": word.get("text"),
            "start_ms": word.get("start"),
            "end_ms": word.get("end"),
            "confidence": word.get("confidence"),
            "speaker": word.get("speaker"),
        }
        for word in result.words
    ]
    return {
        "provider": "AssemblyAI",
        "transcript_id": result.transcript_id,
        "granularity": "word",
        "words": words,
    }
