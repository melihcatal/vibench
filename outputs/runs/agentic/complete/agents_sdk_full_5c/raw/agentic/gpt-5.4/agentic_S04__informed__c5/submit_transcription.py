from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import submit_batch_transcription
from speech_models import BatchTranscriptionRequest, normalize_transcript


def submit_transcription(
    audio_url: str,
    language_code: str = "en_us",
    webhook_url: Optional[str] = None,
    custom_spelling: Optional[list[dict[str, str]]] = None,
) -> Dict[str, Any]:
    request = BatchTranscriptionRequest(
        audio_url=audio_url,
        language_code=language_code,
        webhook_url=webhook_url,
        custom_spelling=custom_spelling,
        punctuate=True,
        format_text=True,
    )
    raw = submit_batch_transcription(request)
    normalized = normalize_transcript(raw)
    return {
        "provider": "AssemblyAI Transcripts API",
        "transcript_id": normalized.transcript_id,
        "status": normalized.status,
        "raw": raw,
    }
