from __future__ import annotations

from typing import Any, Dict, List, Optional

from speech_client import AssemblyAIClient
from speech_models import (
    TranscriptionSubmission,
    normalize_transcript_response,
    segment_dicts,
    transcript_segments_from_utterances,
)


def diarized_transcript(
    audio_url: str, language_code: Optional[str] = None
) -> Dict[str, Any]:
    client = AssemblyAIClient()
    request = TranscriptionSubmission(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=True,
    )
    submitted = client.submit_transcript(request.to_assemblyai_payload())
    transcript = normalize_transcript_response(client.get_transcript(submitted["id"]))
    segments = transcript_segments_from_utterances(transcript.utterances)
    return {
        "id": transcript.id,
        "status": transcript.status,
        "segments": segment_dicts(segments),
        "provider": "assemblyai",
    }
