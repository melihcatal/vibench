from __future__ import annotations

from typing import Any, Dict, List, Optional

from speech_client import get_speech_client
from speech_models import TranscriptionJobRequest, normalize_transcript_response



def diarized_transcript(audio_url: str, language_code: Optional[str] = None) -> Dict[str, Any]:
    client = get_speech_client()
    request = TranscriptionJobRequest(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=True,
    )
    created = client.post("transcript", request.to_assemblyai_payload())
    transcript_id = created["id"]
    fetched = client.get(f"transcript/{transcript_id}")
    result = normalize_transcript_response(fetched)
    utterances: List[Dict[str, Any]] = [
        {
            "speaker": u.speaker,
            "text": u.text,
            "start_ms": u.start_ms,
            "end_ms": u.end_ms,
            "confidence": u.confidence,
        }
        for u in result.utterances
    ]
    return {
        "provider": "AssemblyAI",
        "speaker_labels": True,
        "transcript_id": result.transcript_id,
        "status": result.status,
        "utterances": utterances,
        "raw": result.raw,
    }
