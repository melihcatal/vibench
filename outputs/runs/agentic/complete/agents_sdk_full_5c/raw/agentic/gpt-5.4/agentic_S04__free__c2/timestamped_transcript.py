from __future__ import annotations

from typing import Any, Dict, Literal, Optional

from speech_client import create_session, raise_for_assemblyai_error, transcript_endpoint
from speech_models import extract_timestamp_items


Granularity = Literal["word", "segment"]


def timestamped_transcript(transcript_id: str, granularity: Granularity = "word") -> Dict[str, Any]:
    session = create_session()
    response = session.get(transcript_endpoint(transcript_id), timeout=60)
    raise_for_assemblyai_error(response)
    data = response.json()
    if data.get("status") != "completed":
        raise RuntimeError(f"AssemblyAI transcript {transcript_id} is not completed")

    return {
        "provider": "AssemblyAI",
        "transcript_id": transcript_id,
        "granularity": granularity,
        "timestamps": extract_timestamp_items(data, granularity=granularity),
    }
