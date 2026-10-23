from __future__ import annotations

from speech_client import AssemblyAISpeechClient
from speech_models import TranscriptionJobRequest


def diarized_transcript(
    audio_url: str, language_code: str = "en_us"
) -> dict[str, object]:
    client = AssemblyAISpeechClient()
    job = client.submit_transcription(
        TranscriptionJobRequest(
            audio_url=audio_url,
            language_code=language_code,
            speaker_labels=True,
        )
    )
    result = client.get_transcription(job["id"])
    return {
        "provider": "AssemblyAI",
        "transcript_id": result.transcript_id,
        "status": result.status,
        "utterances": [
            {
                "speaker": segment.speaker,
                "text": segment.text,
                "start_ms": segment.start_ms,
                "end_ms": segment.end_ms,
            }
            for segment in result.segments
        ],
    }
