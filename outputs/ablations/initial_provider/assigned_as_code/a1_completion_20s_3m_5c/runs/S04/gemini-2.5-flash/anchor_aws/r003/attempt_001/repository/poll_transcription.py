import time
import json
import urllib.request

from speech_client import SpeechClient
from speech_models import TranscriptionJob

def poll_transcription(job_id: str, config: dict = None) -> TranscriptionJob:
    config = config or {}
    region = config.get("region")
    if not region:
        raise ValueError("AWS region must be provided in config.")

    speech_client = SpeechClient(region_name=region)
    client = speech_client.get_transcribe_client()

    while True:
        response = client.get_transcription_job(TranscriptionJobName=job_id)
        job_status = response["TranscriptionJob"]["TranscriptionJobStatus"]

        if job_status == "COMPLETED":
            transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            # Fetch the content from the S3 URI
            with urllib.request.urlopen(transcript_uri) as url:
                data = json.loads(url.read().decode())
            
            # For simplicity, returning a raw representation of the transcript data here.
            # In a real application, this would be parsed into TranscriptionResult.
            return TranscriptionJob(job_id=job_id, status=job_status, transcript_uri=data)
        elif job_status == "FAILED":
            raise Exception(f"Transcription job {job_id} failed.")
        else:
            print(f"Transcription job {job_id} is {job_status}. Waiting...")
            time.sleep(10)
