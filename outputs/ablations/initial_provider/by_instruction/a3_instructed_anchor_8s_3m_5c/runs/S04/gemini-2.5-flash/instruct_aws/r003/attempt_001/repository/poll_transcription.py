import time
import requests
from speech_client import get_transcribe_client
from speech_models import TranscriptionJobStatus, TranscriptionResult

def poll_transcription_job(job_name: str, interval_seconds: int = 10, max_retries: int = 60) -> TranscriptionJobStatus:
    transcribe_client = get_transcribe_client()
    retries = 0
    while retries < max_retries:
        try:
            response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            job = response['TranscriptionJob']
            status = job['TranscriptionJobStatus']
            transcript_file_uri = job.get('Transcript', {}).get('TranscriptFileUri')
            failure_reason = job.get('FailureReason')

            print(f"Transcription job {job_name} status: {status}")
            if status == 'COMPLETED':
                return TranscriptionJobStatus(job_name=job_name, status=status, transcript_file_uri=transcript_file_uri)
            elif status == 'FAILED':
                return TranscriptionJobStatus(job_name=job_name, status=status, failure_reason=failure_reason)

            time.sleep(interval_seconds)
            retries += 1
        except Exception as e:
            print(f"Error polling transcription job: {e}")
            raise
    return TranscriptionJobStatus(job_name=job_name, status="TIMEOUT", failure_reason="Max retries reached")

def get_transcript_content(transcript_uri: str) -> str:
    try:
        response = requests.get(transcript_uri)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching transcript from URI {transcript_uri}: {e}")
        raise

def get_transcription_result(job_name: str) -> TranscriptionResult:
    job_status = poll_transcription_job(job_name)
    if job_status.status == 'COMPLETED' and job_status.transcript_file_uri:
        transcript_json_content = get_transcript_content(job_status.transcript_file_uri)
        # In a real scenario, you'd parse the JSON to extract transcript_text, word_timestamps, etc.
        # For this exercise, we'll return the raw JSON content as the text for simplicity.
        # A more robust implementation would parse this JSON into the TranscriptionResult dataclass.
        return TranscriptionResult(
            job_name=job_name,
            status=job_status.status,
            transcript_text=transcript_json_content, # Simplified: returning raw JSON for demonstration
            word_timestamps=None, # Requires parsing the JSON output
            segments=None, # Requires parsing the JSON output
            speaker_labels=None # Requires parsing the JSON output
        )
    else:
        return TranscriptionResult(
            job_name=job_name,
            status=job_status.status,
            transcript_text=None,
            word_timestamps=None,
            segments=None,
            speaker_labels=None
        )
