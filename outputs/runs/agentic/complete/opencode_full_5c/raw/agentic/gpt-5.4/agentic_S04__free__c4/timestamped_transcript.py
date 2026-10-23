from __future__ import annotations

from speech_client import AssemblyAISpeechClient
from speech_models import normalize_words


def timestamped_transcript(
    transcript_id: str, granularity: str = "word"
) -> dict[str, object]:
    client = AssemblyAISpeechClient()
    payload = client.get_raw_transcription(transcript_id)
    if granularity == "segment":
        items = [
            {
                "text": utterance.get("text", ""),
                "start_ms": utterance.get("start", 0),
                "end_ms": utterance.get("end", 0),
                "speaker": utterance.get("speaker"),
            }
            for utterance in payload.get("utterances") or []
        ]
    else:
        items = normalize_words(payload)
    return {
        "provider": "AssemblyAI",
        "transcript_id": payload.get("id", ""),
        "status": payload.get("status", "queued"),
        "granularity": granularity,
        "items": items,
    }
