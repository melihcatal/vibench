# poll_transcription.py
import os
import json
import boto3
import time
from speech_client import SpeechClient
from speech_models import SpeechModels

# Example: python poll_transcription.py my_job_name
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: poll_transcription.py <job_name>", file=sys.stderr)
        sys.exit(1)
    job_name = sys.argv[1]

    client = SpeechClient.get_client()
    while True:
        resp = client.get_transcription_job(TranscriptionJobName=job_name)
        status = resp['TranscriptionJob']['TranscriptionJobStatus']
        print(f"Current status: {status}")
        if status in ("COMPLETED", "FAILED", "PARTIAL_RESULTS"):
            break
        time.sleep(5)  # poll interval

    print(json.dumps(resp, indent=2))
