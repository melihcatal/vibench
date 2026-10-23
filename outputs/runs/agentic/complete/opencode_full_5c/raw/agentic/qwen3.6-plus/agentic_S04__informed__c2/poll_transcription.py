import time

import assemblyai as aai

from speech_client import load_assemblyai_config
from speech_models import (
    PollResult,
    PollResultData,
    TranscriptionResult,
    TranscriptionStatus,
    normalize_assemblyai_response,
)


def poll_transcription(job_id: str) -> PollResultData:
    config = load_assemblyai_config()
    aai.settings.api_key = config.api_key

    transcriber = aai.Transcriber()
    transcript = transcriber.get_transcription(job_id)

    status_map = {
        aai.TranscriptStatus.queued: TranscriptionStatus.QUEUED,
        aai.TranscriptStatus.processing: TranscriptionStatus.PROCESSING,
        aai.TranscriptStatus.completed: TranscriptionStatus.COMPLETED,
        aai.TranscriptStatus.error: TranscriptionStatus.ERROR,
    }

    current_status = status_map.get(transcript.status, TranscriptionStatus.ERROR)

    if (
        current_status == TranscriptionStatus.PROCESSING
        or current_status == TranscriptionStatus.QUEUED
    ):
        return PollResultData(
            result=PollResult.STILL_PROCESSING,
            status=current_status,
            job_id=job_id,
        )

    if current_status == TranscriptionStatus.ERROR:
        return PollResultData(
            result=PollResult.FAILED,
            status=current_status,
            job_id=job_id,
            error_message=transcript.error,
        )

    transcription_result = TranscriptionResult(
        job_id=job_id,
        status=TranscriptionStatus.COMPLETED,
        text=transcript.text,
        audio_duration_ms=int(transcript.audio_duration * 1000)
        if transcript.audio_duration
        else 0,
        language=transcript.language_code or "",
        confidence=transcript.confidence or 0.0,
    )

    return PollResultData(
        result=PollResult.SUCCESS,
        status=TranscriptionStatus.COMPLETED,
        job_id=job_id,
        transcription=transcription_result,
    )


def poll_transcription_with_retry(
    job_id: str, max_attempts: int = None, interval_seconds: int = None
) -> TranscriptionResult:
    config = load_assemblyai_config()
    max_attempts = max_attempts or config.max_poll_attempts
    interval_seconds = interval_seconds or config.polling_interval_seconds

    for attempt in range(max_attempts):
        poll_data = poll_transcription(job_id)

        if poll_data.result == PollResult.SUCCESS:
            return poll_data.transcription

        if poll_data.result == PollResult.FAILED:
            raise RuntimeError(
                f"Transcription job {job_id} failed: {poll_data.error_message}"
            )

        time.sleep(interval_seconds)

    raise TimeoutError(
        f"Transcription job {job_id} did not complete within {max_attempts} attempts"
    )
