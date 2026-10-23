from __future__ import annotations

from typing import Any, Dict, List, Optional

from speech_client import create_session, raise_for_assemblyai_error, transcript_endpoint
from speech_models import TranscriptionJobRequest, normalize_transcript_response


ASSEMBLYAI_SPEECH_MODEL = "best"


def diarized_transcript(
    audio_url: str,
    speakers_expected: Optional[int] = None,
    language_code: Optional[str] = None,
) -> Dict[str, Any]:
    session = create_session()
    request = TranscriptionJobRequest(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=True,
        speakers_expected=speakers_expected,
    )
    payload = request.to_assemblyai_payload()
    payload["speech_model"] = ASSEMBLYAI_SPEECH_MODEL

    response = session.post(transcript_endpoint(), json=payload, timeout=60)
    raise_for_assemblyai_error(response)
    submitted = response.json()
    transcript_id = submitted["id"]

    poll_response = session.get(transcript_endpoint(transcript_id), timeout=60)
    raise_for_assemblyai_error(poll_response)
    result = normalize_transcript_response(poll_response.json())

    utterances: List[Dict[str, Any]] = [
        {
            "speaker": item.speaker,
            "text": item.text,
            "start_ms": item.start_ms,
            "end_ms": item.end_ms,
            "confidence": item.confidence,
        }
        for item in result.utterances
    ]

    return {
        "provider": "AssemblyAI",
        "transcript_id": result.transcript_id,
        "status": result.status,
        "utterances": utterances,
    }
