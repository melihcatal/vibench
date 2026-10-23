import os
import time
import boto3
from speech_client import SpeechClient

# Amazon Transcribe example
client = SpeechClient(service="Amazon Transcribe")

def poll_transcription(job_id: str, wait_seconds: int = 5, max_attempts: int = 20):
    """Poll a batch transcription job and return the transcript when complete.

    Args:
        job_id (str): The transcription job ID returned from submit_transcription.
        wait_seconds (int): Seconds to wait between polls.
        max_attempts (int): Maximum number of poll attempts.

    Returns:
        dict: Final transcription output including results and metadata.
    """
    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        response = client.get_transcription_job(job_id=job_id)
        status = response.get("TranscriptionJob").get("TranscriptionJobStatus")
        if status == "COMPLETED":
            result = response.get("TranscriptionJob").get("Transcript", {}).get("TranscriptFileUri")
            # Retrieve result file contents (placeholder; actual download logic would go here)
            transcript = client.download_transcript(result)
            return {"status": status, "transcript": transcript}
        elif status == "FAILED":
            raise RuntimeError(f"Transcription job failed: {response.get('TranscriptionJob').get('FailureReason')}"),
        print(f"Attempt {attempt}/{max_attempts} - Job status: {status}. Waiting {wait_seconds}s...")
        time.sleep(wait_seconds)
    raise TimeoutError("Transcription job did not complete within the maximum attempts.")
