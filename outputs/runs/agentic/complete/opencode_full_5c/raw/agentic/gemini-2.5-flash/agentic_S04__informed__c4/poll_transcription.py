import os
import time
import assemblyai as aai
from speech_client import get_assemblyai_client


def poll_transcription_job(job_id: str) -> str:
    """Polls an AssemblyAI transcription job and returns the transcript."""
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    client = get_assemblyai_client()
    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{job_id}"

    while True:
        transcript = client.transcripts.get(job_id)
        if transcript.status == aai.TranscriptStatus.completed:
            return transcript.text
        elif transcript.status == aai.TranscriptStatus.error:
            raise RuntimeError(f"Transcription failed: {transcript.error}")
        else:
            time.sleep(5)  # Wait for 5 seconds before polling again


if __name__ == "__main__":
    # Example usage (replace with actual job ID)
    # transcript_text = poll_transcription_job("YOUR_JOB_ID")
    # print(f"Transcription result: {transcript_text}")
    pass
