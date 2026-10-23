import time
import boto3
from speech_client import SpeechClient

client = SpeechClient()  # boto3 helper


def poll_transcription(job_id, wait_seconds=5):
    """Polls the transcription job until completion and returns the transcript URL.
    Raises an error if the job fails or times out.
    """
    while True:
        response = client.transcribe.get_transcription_job(TranscriptionJobName=job_id)
        status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        if status == "COMPLETED":
            url = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            return url
        elif status == "FAILED":
            raise RuntimeError(
                f"Transcription job failed: {response['TranscriptionJob']['FailureReason']}"
            )
        print(f"Job {job_id} still {status}. Waiting {wait_seconds}s...")
        time.sleep(wait_seconds)
