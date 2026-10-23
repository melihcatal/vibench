import os
import time
from assemblyai import Client, TranscriptStatus


def poll_transcription_job(transcript_id: str, timeout_seconds: int = 600) -> dict:
    """
    Polls an AssemblyAI transcription job and returns the transcript.
    """
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    client = Client(api_key=api_key)

    start_time = time.time()
    while True:
        transcript = client.transcripts.get(transcript_id)

        if transcript.status == TranscriptStatus.completed:
            return transcript.json()
        elif transcript.status == TranscriptStatus.error:
            raise RuntimeError(f"Transcription job failed: {transcript.error}")

        if time.time() - start_time > timeout_seconds:
            raise TimeoutError(
                f"Transcription polling timed out after {timeout_seconds} seconds."
            )

        time.sleep(5)  # Wait for 5 seconds before polling again
