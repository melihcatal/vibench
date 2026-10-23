# timestamped_transcript.py
import os
import json
import boto3
import time
from speech_client import SpeechClient
from speech_models import SpeechModels

# Example: python timestamped_transcript.py my_job_name
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: timestamped_transcript.py <job_name>", file=sys.stderr)
        sys.exit(1)
    job_name = sys.argv[1]

    client = SpeechClient.get_client()
    while True:
        resp = SpeechClient.get_job_status(job_name)
        if SpeechModels.is_job_complete(resp):
            break
        time.sleep(5)

    # Assuming timestamp support is enabled; AWS Transcribe provides $results$item$alternatives$timestamps when requested
    transcript_obj = resp['TranscriptionJob']['Transcript']['TranscriptFileUri']
    # Retrieve transcript file (S3 GET)
    s3 = boto3.resource('s3')
    obj = s3.Object(os.getenv('AWS_S3_BUCKET'), transcript_obj)
    transcript_content = json.loads(obj.get()['Body'].read().decode())
    # Example JSON structure extraction; adjust based on actual provider format
    timestamps = SpeechModels.extract_timestamps(transcript_content)
    print(json.dumps(timestamps, indent=2))
