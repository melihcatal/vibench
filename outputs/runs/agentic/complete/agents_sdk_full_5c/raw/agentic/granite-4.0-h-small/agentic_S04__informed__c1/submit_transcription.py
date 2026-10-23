# submit_transcription.py
import os
import json
import boto3
from speech_client import SpeechClient
from speech_models import SpeechModels

# Example: usage: python submit_transcription.py my_job_name s3://my-bucket/audio.wav my-output-bucket
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: submit_transcription.py <job_name> <media_uri> <output_bucket>", file=sys.stderr)
        sys.exit(1)
    job_name = sys.argv[1]
    media_uri = sys.argv[2]
    output_bucket = sys.argv[3]
    # Basic language detection (default en-US; can be extended)
    lang_code = SpeechModels.validate_language_code(os.getenv("LANGUAGE_CODE", "en-US"))

    # Submit the job
    resp = SpeechClient.submit_job(job_name, media_uri, output_bucket, lang_code)
    print(json.dumps(resp, indent=2))
