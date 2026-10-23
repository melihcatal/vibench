import time
from typing import Optional

from speech_client import get_transcription_result
from speech_models import TranscriptionResult

POLL_INTERVAL_SECONDS = 5
MAX_POLL_ATTEMPTS = 300


def poll_transcription_job(
    transcript_id: str,
    poll_interval: float = POLL_INTERVAL_SECONDS,
    max_attempts: int = MAX_POLL_ATTEMPTS,
) -> TranscriptionResult:
    for attempt in range(max_attempts):
        response = get_transcription_result(transcript_id)
        status = response.get("status", "")

        if status == "completed":
            return TranscriptionResult.from_assemblyai_response(response)
        elif status == "error":
            raise RuntimeError(
                f"Transcription job {transcript_id} failed: {response.get('error', 'Unknown error')}"
            )

        time.sleep(poll_interval)

    raise TimeoutError(
        f"Transcription job {transcript_id} did not complete within {max_attempts * poll_interval} seconds"
    )


def get_transcript_text(transcript_id: str) -> str:
    result = poll_transcription_job(transcript_id)
    return result.text


def check_transcription_status(transcript_id: str) -> dict:
    response = get_transcription_result(transcript_id)
    return {
        "transcript_id": response["id"],
        "status": response["status"],
        "audio_duration": response.get("audio_duration", 0),
    }
