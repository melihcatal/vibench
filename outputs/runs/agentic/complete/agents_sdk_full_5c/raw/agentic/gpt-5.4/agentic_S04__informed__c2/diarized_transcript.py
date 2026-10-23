from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import build_speech_client
from speech_models import TranscriptionSubmission, TranscriptStatus, normalize_segments


def diarized_transcript(
    transcript_id: Optional[str] = None,
    audio_path: Optional[str] = None,
    audio_url: Optional[str] = None,
    speakers_expected: Optional[int] = None,
) -> Dict[str, Any]:
    client = build_speech_client()

    if transcript_id:
        transcript = TranscriptStatus.from_assemblyai(client.get_transcript(transcript_id))
    else:
        resolved_audio_url = audio_url or (client.upload_audio(audio_path) if audio_path else None)
        if not resolved_audio_url:
            raise ValueError("transcript_id or audio_path or audio_url is required")
        request = TranscriptionSubmission(
            audio_url=resolved_audio_url,
            speaker_labels=True,
            speakers_expected=speakers_expected,
        )
        created = client.submit_transcript(request.to_assemblyai_payload())
        transcript = TranscriptStatus.from_assemblyai(client.get_transcript(created["id"]))

    utterances = normalize_segments(transcript, granularity="segment")
    return {
        "provider": "AssemblyAI",
        "transcript_id": transcript.id,
        "status": transcript.status,
        "utterances": [
            {
                "speaker": item.speaker,
                "text": item.text,
                "start_ms": item.start_ms,
                "end_ms": item.end_ms,
                "confidence": item.confidence,
            }
            for item in utterances
        ],
    }
