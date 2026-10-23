# HELPER - Local configuration and client utilities for AWS Transcribe (Batch Speech-to-Text)
import os
import boto3

# AWS credentials (expected to be set in the environment)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

# Create a reusable Transcribe client
transcribe_client = boto3.client(
    "transcribe",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


# Helper to build the request payload for a transcription job
# (can be extended for other providers in future)
def build_transcription_request(
    job_name, audio_uri, language="en-US", show_diarization=False
):
    payload = {
        "TranscriptionJobName": job_name,
        "Media": {"MediaFileUri": audio_uri},
        "MediaFormat": "mp3",  # adjust based on actual file format
        "LanguageCode": language,
    }
    if show_diarization:
        payload["Settings"] = {
            "ShowSpeakerLabels": True,
            "MaxSpeakerLabels": 10,
        }
    return payload


# Helper to wait for a job and return its output URL
# (this can be adapted for other SDKs by swapping client calls)
def wait_for_job(job_name, interval=10):
    while True:
        resp = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        status = resp["TranscriptionJob"]["TranscriptionJobStatus"]
        if status in ("COMPLETED", "FAILED"):
            break
        time.sleep(interval)
    if status == "COMPLETED":
        return resp["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    raise RuntimeError(f"Job {job_name} failed")
