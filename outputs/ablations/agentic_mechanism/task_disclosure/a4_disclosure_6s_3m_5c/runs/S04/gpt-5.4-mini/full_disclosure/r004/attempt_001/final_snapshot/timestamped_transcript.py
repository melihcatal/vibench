import os
from typing import Any, Dict, List, Optional

import requests


ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"


def _extract_timestamps(transcript: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    words = transcript.get("words") or []
    segments = transcript.get("segments") or transcript.get("utterances") or []
    return {"words": words, "segments": segments}


def timestamped_transcript(transcript_id: str, *, api_key: Optional[str] = None) -> Dict[str, Any]:
    token = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
    if not token:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")

    response = requests.get(
        f"{ASSEMBLYAI_BASE_URL}/transcript/{transcript_id}",
        headers={"authorization": token},
        timeout=30,
    )
    response.raise_for_status()
    transcript = response.json()
    timestamps = _extract_timestamps(transcript)
    return {
        "transcript_id": transcript_id,
        "status": transcript.get("status"),
        "words": timestamps["words"],
        "segments": timestamps["segments"],
        "response": transcript,
    }
