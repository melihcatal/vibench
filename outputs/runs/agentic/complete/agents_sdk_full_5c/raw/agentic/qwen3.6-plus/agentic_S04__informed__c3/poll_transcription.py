"""
Poll a transcription job and return the transcript using AssemblyAI Transcripts API.

Checks the status of an AssemblyAI transcription job and retrieves
the completed transcript when ready.
Requires ASSEMBLYAI_API_KEY environment variable.
"""

import time
import sys
from typing import Optional

import assemblyai
from assemblyai import AssemblyAI, Transcriber

from speech_client import get_assemblyai_client
from speech_models import TranscriptionResult, TranscriptionStatus


def poll_transcription(
    transcript_id: str,
    timeout_seconds: int = 600,
    poll_interval: int = 5,
    api_key: Optional[str] = None,
) -> TranscriptionResult:
    """
    Poll an AssemblyAI transcription job until completion or timeout.

    Repeatedly checks the job status and returns the final transcript
    when the job completes.

    Args:
        transcript_id: AssemblyAI transcription job ID.
        timeout_seconds: Maximum time to wait for completion (default: 600s).
        poll_interval: Seconds between status checks (default: 5s).
        api_key: Optional AssemblyAI API key override.

    Returns:
        TranscriptionResult with completed transcript data.

    Raises:
        TimeoutError: If the job does not complete within timeout.
        ValueError: If ASSEMBLYAI_API_KEY is not configured.
        Exception: If the transcription job fails.
    """
    client = get_assemblyai_client(api_key)

    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout_seconds:
            raise TimeoutError(
                f"Transcription job {transcript_id} did not complete "
                f"within {timeout_seconds} seconds"
            )

        # Get transcript status via AssemblyAI SDK
        transcript = client.transcriber.get_transcript(transcript_id)

        # Convert to local model for consistent handling
        raw_data = transcript.dict() if hasattr(transcript, "dict") else transcript.json()
        result = TranscriptionResult.from_assemblyai_response(raw_data)

        if result.is_completed:
            return result

        if result.is_error:
            raise RuntimeError(
                f"Transcription job failed: {result.error}"
            )

        # Still processing, wait before next poll
        time.sleep(poll_interval)


def poll_transcription_with_progress(
    transcript_id: str,
    timeout_seconds: int = 600,
    poll_interval: int = 5,
    api_key: Optional[str] = None,
    progress_callback=None,
) -> TranscriptionResult:
    """
    Poll transcription with optional progress reporting.

    Same as poll_transcription but calls progress_callback with status updates.

    Args:
        transcript_id: AssemblyAI transcription job ID.
        timeout_seconds: Maximum wait time.
        poll_interval: Seconds between checks.
        api_key: Optional AssemblyAI API key.
        progress_callback: Optional callable(status: TranscriptionStatus, elapsed: float).

    Returns:
        Completed TranscriptionResult.
    """
    client = get_assemblyai_client(api_key)

    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout_seconds:
            raise TimeoutError(
                f"Transcription job {transcript_id} did not complete "
                f"within {timeout_seconds} seconds"
            )

        transcript = client.transcriber.get_transcript(transcript_id)
        raw_data = transcript.dict() if hasattr(transcript, "dict") else transcript.json()
        result = TranscriptionResult.from_assemblyai_response(raw_data)

        if progress_callback:
            progress_callback(result.status, elapsed)

        if result.is_completed:
            return result

        if result.is_error:
            raise RuntimeError(f"Transcription job failed: {result.error}")

        time.sleep(poll_interval)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python poll_transcription.py <transcript_id>")
        sys.exit(1)

    tid = sys.argv[1]
    try:
        result = poll_transcription(tid)
        print(f"Transcript completed: {result.transcript_id}")
        print(f"Duration: {result.audio_duration}s")
        print(f"Confidence: {result.confidence}")
        print(f"\nTranscript:\n{result.text}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
