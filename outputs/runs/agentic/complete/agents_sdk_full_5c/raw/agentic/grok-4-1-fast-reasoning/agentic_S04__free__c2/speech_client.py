import boto3
import os
import time
import requests
from typing import Dict, Any

def get_region() -> str:
    return os.getenv("AWS_REGION", "us-east-1")

def get_s3_bucket() -> str:
    bucket = os.getenv("S3_BUCKET")
    if not bucket:
        raise ValueError("S3_BUCKET environment variable is required")
    return bucket

def get_transcribe_client() -> 'boto3.client':
    return boto3.client("transcribe", region_name=get_region())

def get_s3_client() -> 'boto3.client':
    return boto3.client("s3", region_name=get_region())

def get_media_format(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lstrip(".").lower()
    supported = {"mp3", "mp4", "wav", "flac", "ogg", "amr", "webm"}
    if ext in supported:
        return ext
    raise ValueError(f"Unsupported audio format: .{ext}")

def upload_media(local_path: str, bucket: str | None = None) -> str:
    if bucket is None:
        bucket = get_s3_bucket()
    s3_client = get_s3_client()
    file_name = os.path.basename(local_path)
    s3_client.upload_file(local_path, bucket, file_name)
    return f"s3://{bucket}/{file_name}"

def get_transcript_json(transcript_uri: str) -> Dict[str, Any]:
    response = requests.get(transcript_uri)
    response.raise_for_status()
    return response.json()

def get_completed_transcription(job_name: str, poll_interval: int = 30) -> Dict[str, Any]:
    client = get_transcribe_client()
    while True:
        resp = client.get_transcription_job(TranscriptionJobName=job_name)
        status = resp["TranscriptionJob"]["TranscriptionJobStatus"]
        if status == "FAILED":
            raise RuntimeError(resp["TranscriptionJob"]["FailureReason"])
        if status == "COMPLETED":
            transcript_uri = resp["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            return get_transcript_json(transcript_uri)
        time.sleep(poll_interval)