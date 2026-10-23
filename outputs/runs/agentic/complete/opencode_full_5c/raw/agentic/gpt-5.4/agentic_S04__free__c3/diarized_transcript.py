from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import AssemblyAIBatchSpeechClient
from speech_models import BatchTranscriptionRequest


def diarized_transcript(
    audio_url: str, language_code: Optional[str] = None
) -> Dict[str, Any]:
    client = AssemblyAIBatchSpeechClient()
    request = BatchTranscriptionRequest(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=True,
    )
    submitted = client.submit_transcription(request)
    job = client.wait_for_completion(submitted.transcript_id)
    return {
        "provider": "AssemblyAI",
        "transcript_id": job.transcript_id,
        "status": job.status,
        "text": job.text,
        "utterances": [
            {
                "speaker": item.speaker,
                "text": item.text,
                "start_ms": item.start_ms,
                "end_ms": item.end_ms,
                "confidence": item.confidence,
            }
            for item in job.utterances
        ],
    }
