import os
from speech_client import post_transcript, get_transcript
import time


def request_diarized_transcript(audio_file_url: str) -> dict:
    """
    Requests speaker diarization for a recorded meeting using AssemblyAI.
    """
    if not os.getenv("ASSEMBLYAI_API_KEY"):
        raise EnvironmentError("ASSEMBLYAI_API_KEY environment variable not set.")

    options = {"speaker_labels": True}
    response = post_transcript(audio_file_url, options)
    job_id = response.get("id")

    if not job_id:
        raise ValueError("Failed to submit transcription job")

    while True:
        result = get_transcript(job_id)
        if result["status"] == "completed":
            return result
        elif result["status"] == "failed":
            raise RuntimeError(f"Transcription failed: {result.get('error')}")
        time.sleep(5)
