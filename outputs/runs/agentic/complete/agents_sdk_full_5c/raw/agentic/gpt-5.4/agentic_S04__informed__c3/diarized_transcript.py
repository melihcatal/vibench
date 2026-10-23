from __future__ import annotations

from typing import Optional

from speech_client import AssemblyAIClient, build_batch_request, ensure_completed


def diarized_transcript(
    audio_url: str,
    speakers_expected: Optional[int] = None,
    language_code: Optional[str] = None,
) -> dict:
    client = AssemblyAIClient()
    submitted = client.submit_transcription(
        build_batch_request(
            audio_url=audio_url,
            language_code=language_code,
            speaker_labels=True,
            speakers_expected=speakers_expected,
        )
    )
    result = ensure_completed(client.get_transcription(submitted.transcript_id))
    utterances = [
        {
            "speaker": segment.speaker,
            "text": segment.text,
            "start_ms": segment.start_ms,
            "end_ms": segment.end_ms,
            "confidence": segment.confidence,
        }
        for segment in result.utterances
    ]
    return {
        "provider": "AssemblyAI",
        "transcript_id": result.transcript_id,
        "status": result.status,
        "utterances": utterances,
    }
