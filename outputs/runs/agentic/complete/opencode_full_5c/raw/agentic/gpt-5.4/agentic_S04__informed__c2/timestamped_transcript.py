from __future__ import annotations

from typing import Any, Dict, List

from speech_client import AssemblyAISpeechClient


def timestamped_transcript(
    transcript_id: str, level: str = "word"
) -> List[Dict[str, Any]]:
    client = AssemblyAISpeechClient()
    response = client.get_transcript(transcript_id)
    if level == "segment":
        return response.get("utterances") or []
    return response.get("words") or []
