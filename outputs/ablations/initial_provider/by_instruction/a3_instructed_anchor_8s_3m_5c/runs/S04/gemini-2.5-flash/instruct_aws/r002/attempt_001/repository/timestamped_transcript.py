import boto3
import os
import json

def get_aws_timestamped_transcript(job_name: str, region_name: str = os.environ.get("AWS_REGION", "us-east-1")):
    """
    Retrieves a completed AWS Transcribe job result with word-level timestamps.
    """
    transcribe_client = boto3.client("transcribe", region_name=region_name)

    response = transcribe_client.get_transcription_job(
        TranscriptionJobName=job_name
    )

    job = response['TranscriptionJob']
    if job['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_file_uri = job['Transcript']['TranscriptFileUri']
        # In a real application, you would download and parse the JSON file from this URI
        # For this example, we'll simulate the structure of a timestamped result.

        # Simulate fetching and parsing the transcript file
        # In a real scenario, you'd make an HTTP GET request to transcript_file_uri
        # and parse the JSON content.
        # Example simulated content:
        simulated_transcript_content = {
            "results": {
                "items": [
                    {"start_time": "0.000", "end_time": "0.500", "type": "pronunciation", "alternatives": [{"content": "Hello"}]},
                    {"start_time": "0.600", "end_time": "1.000", "type": "pronunciation", "alternatives": [{"content": "world"}]},
                    {"type": "punctuation", "alternatives": [{"content": "!"}]},
                ]
            }
        }
        return simulated_transcript_content
    elif job['TranscriptionJobStatus'] == 'FAILED':
        raise Exception(f"AWS Transcribe job failed: {job.get('FailureReason')}")
    else:
        return {"status": job['TranscriptionJobStatus'], "message": "Transcription job not yet completed."}
