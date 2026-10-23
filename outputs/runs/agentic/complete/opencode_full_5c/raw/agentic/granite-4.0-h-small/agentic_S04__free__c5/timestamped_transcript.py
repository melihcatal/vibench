import os
import requests

# provider: AWS Transcribe
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = "us-east-1"
BASE_URL = f"https://{AWS_REGION}.transcribe.amazonaws.com"

import boto3

client = boto3.client(
    "transcribe",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)


def timestamped_transcript(job_name):
    """
    Retrieve a transcription job result with word-level timestamps from AWS Transcribe.
    Returns a list of dicts: [{"start": ..., "end": ..., "text": ...}, ...]
    """
    while True:
        response = client.get_transcription_job(TranscriptionJobName=job_name)
        status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        if status == "COMPLETED":
            result_url = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            break
        elif status == "FAILED":
            raise RuntimeError(
                f"Transcription job failed: {response['TranscriptionJob']['FailureReason']}"
            )
        time.sleep(5)
    # Download transcript JSON
    import urllib.request

    with urllib.request.urlopen(result_url) as resp:
        data = json.load(resp)
    items = data.get("results", {}).get("items", [])
    timestamps = []
    for item in items:
        if item["type"] == "content":
            start = item.get("start_time")
            end = item.get("end_time")
            text = item.get("content", "")
            timestamps.append({"start": start, "end": end, "text": text})
    return timestamps
