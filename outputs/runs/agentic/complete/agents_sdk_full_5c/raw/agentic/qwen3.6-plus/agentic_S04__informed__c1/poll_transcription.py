"""Poll a transcription job and return the transcript using AssemblyAI Transcripts API."""

import time
from typing import Optional

import assemblyai as aai

from speech_client import create_client, extract_transcript_id, format_transcript_text
from speech_models import TranscriptionResponse


def poll_transcription(
    job_id: str,
    timeout_seconds: int = 300,
    poll_interval_seconds: int = 5,
    api_key: Optional[str] = None,
) -> TranscriptionResponse:
    """Poll an AssemblyAI transcription job until completion or timeout.

    Args:
        job_id: The transcript job ID returned from submission.
        timeout_seconds: Maximum time to wait for completion.
        poll_interval_seconds: Seconds between polling attempts.
        api_key: Optional AssemblyAI API key; falls back to environment.

    Returns:
        TranscriptionResponse containing the transcript text and segments.
    """
    client = create_client(api_key)
    transcriber = aai.Transcriber()

    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        transcript = transcriber.get_transcript(job_id)

        if transcript.status == aai.TranscriptStatus.completed:
            return TranscriptionResponse.from_assemblyai_transcript(transcript)

        if transcript.status == aai.TranscriptStatus.error:
            raise RuntimeError(f"Transcription failed: {transcript.error}")

        if transcript.status == aai.TranscriptStatus.queued:
            print(f"Job {job_id} is queued, waiting {poll_interval_seconds}s...")
        else:
            print(f"Job {job_id} is processing, waiting {poll_interval_seconds}s...")

        time.sleep(poll_interval_seconds)

    raise TimeoutError(
        f"Transcription job {job_id} did not complete within {timeout_seconds}s"
    )


def get_transcript_text(
    job_id: str,
    timeout_seconds: int = 300,
    api_key: Optional[str] = None,
) -> str:
    """Convenience function to get just the transcript text from a job."""
    response = poll_transcription(job_id, timeout_seconds=timeout_seconds, api_key=api_key)
    return response.text


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python poll_transcription.py <job_id>")
        sys.exit(1)
    result = poll_transcription(sys.argv[1])
    print(f"Transcript for job {result.job_id}:")
    print(result.text)
