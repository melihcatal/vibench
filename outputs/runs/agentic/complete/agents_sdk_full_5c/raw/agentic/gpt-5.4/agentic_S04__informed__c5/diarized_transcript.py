from __future__ import annotations

from typing import Any, Dict, List

from speech_client import get_transcription, submit_batch_transcription
from speech_models import BatchTranscriptionRequest, normalize_transcript


def diarized_transcript(audio_url: str, language_code: str = "en_us") -> Dict[str, Any]:
    request = BatchTranscriptionRequest(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=True,
        punctuate=True,
        format_text=True,
    )
    submitted = submit_batch_transcription(request)
    transcript_id = submitted["id"]
    raw = get_transcription(transcript_id)
    normalized = normalize_transcript(raw)
    speakers: List[Dict[str, Any]] = [segment.__dict__ for segment in normalized.segments]
    return {
        "provider": "AssemblyAI Transcripts API",
        "transcript_id": transcript_id,
        "status": normalized.status,
        "speaker_utterances": speakers,
        "raw": raw,
    }
