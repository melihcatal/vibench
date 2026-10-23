import time
import urllib.request
import json
from typing import Dict, Any

from speech_client import get_transcribe_client
from speech_models import normalize_transcription_job_status, normalize_transcript_result

def poll_transcription(job_id: str, config: Dict[str, Any] = None):
    config = config or {}
    client = get_transcribe_client(region_name=config.get("region"))

    while True:
        response = client.get_transcription_job(TranscriptionJobName=job_id)
        job_status = normalize_transcription_job_status(response)
        status = job_status["status"]

        if status == "COMPLETED":
            transcript_uri = job_status["transcript_file_uri"]
            with urllib.request.urlopen(transcript_uri) as url:
                data = json.loads(url.read().decode())
            return normalize_transcript_result(data)
        elif status == "FAILED":
            raise Exception(f"Transcription job failed: {job_status['failure_reason']}")
        
        print(f"Transcription job {job_id} is {status}. Waiting...")
        time.sleep(config.get("poll_interval_seconds", 5))
