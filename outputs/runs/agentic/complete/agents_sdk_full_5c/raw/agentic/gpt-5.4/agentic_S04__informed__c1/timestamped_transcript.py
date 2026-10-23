from __future__ import annotations

from typing import Any, Dict, Literal

from speech_client import AssemblyAISpeechClient
from speech_models import normalize_utterances, normalize_words


def timestamped_transcript(
    transcript_id: str,
    granularity: Literal["word", "segment"] = "word",
) -> Dict[str, Any]:
    client = AssemblyAISpeechClient()
    result = client.get_transcription(transcript_id)
    items = normalize_words(result) if granularity == "word" else normalize_utterances(result)
    return {
        "provider": "AssemblyAI",
        "id": result.get("id", transcript_id),
        "status": result.get("status"),
        "granularity": granularity,
        "timestamps": items,
    }
