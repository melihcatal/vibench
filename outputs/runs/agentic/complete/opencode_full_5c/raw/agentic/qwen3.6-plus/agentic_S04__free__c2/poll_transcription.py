import sys
import json
from typing import Optional

from speech_models import TranscriptionResult, TranscriptionStatus
from speech_client import (
    get_transcription_status,
    get_transcription_result,
    poll_until_complete,
    get_assemblyai_config,
)


def poll_transcription(
    job_id: str,
    wait_for_completion: bool = True,
    poll_interval: float = 5.0,
    max_wait: float = 600.0,
) -> dict:
    config = get_assemblyai_config()
    if wait_for_completion:
        result = poll_until_complete(
            job_id, config, interval=poll_interval, max_wait=max_wait
        )
    else:
        job = get_transcription_status(job_id, config)
        if job.status == TranscriptionStatus.COMPLETED:
            result = get_transcription_result(job_id, config)
        else:
            return {
                "job_id": job.job_id,
                "status": job.status.value,
                "message": "Transcription not yet complete",
            }
    return {
        "job_id": result.job_id,
        "status": result.status,
        "text": result.text,
        "confidence": result.confidence,
        "audio_duration": result.audio_duration,
        "language_code": result.language_code,
        "word_count": len(result.words),
        "utterance_count": len(result.utterances),
    }


def get_transcript_text(
    job_id: str,
    wait_for_completion: bool = True,
    poll_interval: float = 5.0,
    max_wait: float = 600.0,
) -> str:
    result = poll_transcription(
        job_id,
        wait_for_completion=wait_for_completion,
        poll_interval=poll_interval,
        max_wait=max_wait,
    )
    return result.get("text", "")


def main():
    if len(sys.argv) < 2:
        print("Usage: python poll_transcription.py <job_id> [--no-wait]")
        sys.exit(1)
    job_id = sys.argv[1]
    wait = "--no-wait" not in sys.argv
    result = poll_transcription(job_id, wait_for_completion=wait)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
