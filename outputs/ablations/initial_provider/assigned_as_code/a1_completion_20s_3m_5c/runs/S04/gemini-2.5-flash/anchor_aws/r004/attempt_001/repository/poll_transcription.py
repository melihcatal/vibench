import time
import urllib.request

import boto3


def poll_transcription(job_id, config=None):
    config = config or {}
    client = boto3.client("transcribe", region_name=config.get("region"))
    while True:
        response = client.get_transcription_job(TranscriptionJobName=job_id)
        job_status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        if job_status == "COMPLETED":
            transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            with urllib.request.urlopen(transcript_uri) as f:
                return f.read().decode("utf-8")
        elif job_status == "FAILED":
            raise Exception(f"Transcription job {job_id} failed.")
        time.sleep(5)
