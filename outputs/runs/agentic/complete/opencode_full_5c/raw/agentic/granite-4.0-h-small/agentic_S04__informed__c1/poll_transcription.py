import os
import assemblyai as aai
import time


def poll_transcription(job_id: str, timeout: int = 180) -> str:
    """Poll a transcription job for completion and return the transcript.

    Returns the final transcript text.
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing ASSEMBLYAI_API_KEY environment variable")

    client = aai.Transcriber(api_key=api_key)
    transcript = client.get_transcript(job_id)
    while transcript.status not in ("completed", "errored"):
        time.sleep(5)
        transcript = client.get_transcript(job_id)
        if transcript.status == "errored":
            raise RuntimeError(f"Transcription failed with error: {transcript.error}")
    return transcript.text
