import os
from speech_client import post_transcript, get_transcript
import time
from typing import List, Dict


def get_timestamped_transcript(audio_file_url: str) -> List[Dict]:
    """
    Returns word or segment timestamps from an AssemblyAI transcription result.
    """
    if not os.getenv("ASSEMBLYAI_API_KEY"):
        raise EnvironmentError("ASSEMBLYAI_API_KEY environment variable not set.")

    options = {"word_timestamps": True}
    response = post_transcript(audio_file_url, options=options)
    job_id = response.get("id")

    if not job_id:
        raise ValueError("Failed to submit transcription job")

    while True:
        result = get_transcript(job_id)
        if result["status"] == "completed":
            return result.get("words", [])
        elif result["status"] == "failed":
            raise RuntimeError(f"Transcription failed: {result.get('error')}")
        time.sleep(5)
