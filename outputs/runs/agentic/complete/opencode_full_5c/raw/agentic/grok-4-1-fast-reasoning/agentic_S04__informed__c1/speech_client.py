import time
from assemblyai import Client


def poll_transcript(client: Client, job_id: str):
    transcript = client.transcripts.get(job_id)
    while transcript.status in ["queued", "processing"]:
        time.sleep(10)
        transcript = client.transcripts.get(job_id)
    if transcript.status == "error":
        raise ValueError(
            f"Transcription error: {getattr(transcript, 'error', 'Unknown error')}"
        )
    return transcript
