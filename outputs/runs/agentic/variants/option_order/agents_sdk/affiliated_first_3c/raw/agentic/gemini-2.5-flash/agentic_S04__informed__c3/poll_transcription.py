import time
from assemblyai import Client, Transcript
from speech_client import get_assemblyai_client

def poll_transcription_job(job_id: str, timeout: int = 300) -> str:
    """Polls a transcription job and returns the transcript from AssemblyAI."""
    client = get_assemblyai_client()
    start_time = time.time()

    while True:
        transcript = client.transcripts.get(job_id)
        if transcript.status == Transcript.Status.completed:
            return transcript.text
        elif transcript.status == Transcript.Status.error:
            raise Exception(f"AssemblyAI transcription job {job_id} failed: {transcript.error}")
        elif time.time() - start_time > timeout:
            raise TimeoutError(f"AssemblyAI transcription job {job_id} timed out.")
        time.sleep(5)  # Wait for 5 seconds before polling again

if __name__ == '__main__':
    # Example usage: Replace with a real job ID
    example_job_id = "your_assemblyai_job_id"
    try:
        transcript_text = poll_transcription_job(example_job_id)
        print(f"Transcription completed:\n{transcript_text}")
    except Exception as e:
        print(f"Error polling transcription job: {e}")
