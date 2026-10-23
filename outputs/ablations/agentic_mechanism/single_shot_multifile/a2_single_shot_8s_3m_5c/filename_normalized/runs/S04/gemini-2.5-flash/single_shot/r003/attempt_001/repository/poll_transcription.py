import time
import requests
import json
import os
from speech_client import get_transcribe_client
from speech_models import TranscriptionJobStatus, TranscriptResult

def poll_transcription_job(job_name: str, timeout_seconds: int = 600, poll_interval_seconds: int = 10) -> TranscriptionJobStatus:
    """
    Polls an AWS Transcribe job until completion or timeout.
    Returns the job status.
    """
    transcribe_client = get_transcribe_client()
    start_time = time.time()

    while True:
        if time.time() - start_time > timeout_seconds:
            raise TimeoutError(f"Transcription job {job_name} timed out after {timeout_seconds} seconds.")

        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job = response["TranscriptionJob"]
        status = job["TranscriptionJobStatus"]

        if status == "COMPLETED":
            transcript_uri = job["Transcript"]["TranscriptFileUri"]
            return TranscriptionJobStatus(job_name=job_name, status=status, transcript_uri=transcript_uri)
        elif status == "FAILED":
            failure_reason = job.get("FailureReason", "Unknown failure")
            return TranscriptionJobStatus(job_name=job_name, status=status, failure_reason=failure_reason)
        else:
            time.sleep(poll_interval_seconds)

def get_transcript_content(transcript_uri: str) -> TranscriptResult:
    """
    Downloads and parses the transcription result from the provided URI, structured for AWS Transcribe output.
    """
    try:
        response = requests.get(transcript_uri)
        response.raise_for_status() 
        transcript_data = json.loads(response.text)
        
        full_text = transcript_data["results"]["transcripts"][0]["transcript"]
        items = transcript_data["results"]["items"]
        segments = transcript_data["results"].get("segments") # Will be None if not present
        
        return TranscriptResult(full_text=full_text, items=items, segments=segments)
    except requests.exceptions.RequestException as e:
        raise IOError(f"Failed to download transcript from {transcript_uri}: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON transcript from {transcript_uri}: {e}")
    except KeyError as e:
        raise ValueError(f"Missing expected key in transcript data: {e}. Data: {transcript_data}")
