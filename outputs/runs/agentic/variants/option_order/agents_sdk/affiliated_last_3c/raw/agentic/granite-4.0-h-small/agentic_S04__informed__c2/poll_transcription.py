import os
import assemblyai as aai
import time

def poll_transcription(job_id: str, poll_interval: int = 5):
    """Poll the transcription job until it is finished.
    Returns the final transcript text.
    """
    client = aai.TranscriptionClient(api_key=os.getenv("ASSEMBLYAI_API_KEY"))
    while True:
        status = client.check_transcription(job_id)
        if status["status"] == "processing":
            time.sleep(poll_interval)
        elif status["status"] == "queued":
            time.sleep(poll_interval)
        elif status["status"] == "error":
            raise RuntimeError(f"Transcription failed: {status.get('error')}")
        else:  # completed
            transcript = client.download_transcript(job_id)
            return transcript["text"]
