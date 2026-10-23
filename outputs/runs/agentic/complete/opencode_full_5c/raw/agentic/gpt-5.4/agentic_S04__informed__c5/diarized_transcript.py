from __future__ import annotations

from typing import Any, Dict, List

from speech_client import assemblyai_post, build_batch_transcription_payload
from speech_models import TranscriptionJobRequest


def request_diarized_transcript(
    audio_url: str,
    language_code: str = "en_us",
    speakers_expected: int | None = None,
) -> Dict[str, Any]:
    request = TranscriptionJobRequest(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=True,
        speakers_expected=speakers_expected,
        word_timestamps=True,
    )
    payload = build_batch_transcription_payload(request)
    payload["speaker_labels"] = True
    result = assemblyai_post("/transcript", payload)
    return {
        "provider": "AssemblyAI",
        "speech_model": payload.get("speech_model", "best"),
        "transcript_id": result["id"],
        "status": result.get("status", "queued"),
        "speaker_labels": True,
    }
