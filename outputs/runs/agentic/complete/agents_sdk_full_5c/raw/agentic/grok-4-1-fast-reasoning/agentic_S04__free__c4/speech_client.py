import os
import time
import assemblyai as aai
from typing import Optional

def get_client() -> aai.Client:
    if not os.getenv("ASSEMBLYAI_API_KEY"):
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required.")
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    return aai.Client()

def poll_for_completion(client: aai.Client, transcript_id: str, interval: float = 30.0, timeout: int = 3600) -> Optional[aai.Transcript]:
    """
    Poll for transcription completion.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        transcript = client.transcripts.get(transcript_id)
        if transcript.status == aai.TranscriptStatus.completed:
            return transcript
        if transcript.status == aai.TranscriptStatus.error or transcript.status == aai.TranscriptStatus.exception:
            raise RuntimeError(f"Transcription failed: {getattr(transcript, 'error', 'Unknown error')}")
        time.sleep(interval)
    raise TimeoutError(f"Polling timed out after {timeout} seconds")