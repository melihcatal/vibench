import os
import assemblyai as aai


def timestamped_transcript(job_id: str) -> list[dict]:
    """Retrieve word-level timestamps for a completed transcription.

    Returns a list of dictionaries, each representing a word with start and end times.
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing ASSEMBLYAI_API_KEY environment variable")

    client = aai.Transcriber(api_key=api_key)
    transcript = client.get_transcript(job_id)
    if transcript.status != "completed":
        raise RuntimeError(
            f"Transcription not yet completed (status: {transcript.status})"
        )
    return transcript.words
