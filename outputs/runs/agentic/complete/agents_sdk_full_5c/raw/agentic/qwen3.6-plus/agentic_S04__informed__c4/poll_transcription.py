"""Poll a transcription job and return the transcript using AssemblyAI Transcripts API.

Uses the AssemblyAI Python SDK (assemblyai) to poll a previously submitted transcription.
Auth: ASSEMBLYAI_API_KEY environment variable.
"""

import sys
import time
from typing import Optional

from assemblyai import Transcriber

from speech_models import TranscriptionResponse, normalize_assemblyai_response


def poll_transcription(
    job_id: str,
    max_wait_seconds: int = 300,
    poll_interval: int = 5,
) -> TranscriptionResponse:
    """Poll an AssemblyAI transcription job until completion or timeout.

    Returns a normalized TranscriptionResponse.
    """
    transcriber = Transcriber()
    transcript = transcriber.get_transcript_by_id(job_id)

    elapsed = 0
    while transcript.status not in ("completed", "error"):
        time.sleep(poll_interval)
        elapsed += poll_interval
        if elapsed >= max_wait_seconds:
            raise TimeoutError(
                f"Transcription job {job_id} did not complete within {max_wait_seconds}s"
            )
        transcript = transcriber.get_transcript_by_id(job_id)

    if transcript.status == "error":
        raise RuntimeError(
            f"Transcription job {job_id} failed: {transcript.error}"
        )

    return normalize_assemblyai_response(transcript)


def main():
    job_id = sys.argv[1] if len(sys.argv) > 1 else None
    if not job_id:
        print("Usage: python poll_transcription.py <job_id>")
        sys.exit(1)

    result = poll_transcription(job_id)
    print(f"Transcription complete for job: {result.job_id}")
    print(f"Status: {result.status}")
    print(f"Duration: {result.duration_sec}s")
    print(f"Transcript:\n{result.transcript}")


if __name__ == "__main__":
    main()
