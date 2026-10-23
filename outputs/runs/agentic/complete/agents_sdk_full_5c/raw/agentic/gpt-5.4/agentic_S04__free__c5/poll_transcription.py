from __future__ import annotations

import time
from typing import Any, Dict

from speech_client import get_speech_client
from speech_models import normalize_transcript_response


TERMINAL_STATES = {"completed", "error"}



def poll_transcription(transcript_id: str, interval_seconds: float = 3.0, max_attempts: int = 40) -> Dict[str, Any]:
    client = get_speech_client()
    last = None
    for _ in range(max_attempts):
        data = client.get(f"transcript/{transcript_id}")
        result = normalize_transcript_response(data)
        last = result
        if result.status in TERMINAL_STATES:
            break
        time.sleep(interval_seconds)
    if last is None:
        raise RuntimeError("No polling attempts were made")
    if last.status == "error":
        raise RuntimeError(last.raw.get("error", "AssemblyAI transcription failed"))
    return {
        "provider": "AssemblyAI",
        "transcript_id": last.transcript_id,
        "status": last.status,
        "text": last.text,
        "utterance_count": len(last.utterances),
        "word_count": len(last.words),
        "raw": last.raw,
    }
