import boto3
from speech_client import get_transcribe_client
from speech_models import TranscriptionJobResult
import time

def poll_transcription_job(job_name: str, timeout_seconds: int = 600, poll_interval_seconds: int = 10) -> TranscriptionJobResult:
    transcribe_client = get_transcribe_client()
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = response['TranscriptionJob']['TranscriptionJobStatus']

        if job_status == 'COMPLETED':
            transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
            return TranscriptionJobResult(job_name=job_name, status=job_status, transcript_file_uri=transcript_uri)
        elif job_status == 'FAILED':
            failure_reason = response['TranscriptionJob'].get('FailureReason', 'Unknown reason')
            return TranscriptionJobResult(job_name=job_name, status=job_status, failure_reason=failure_reason)
        
        print(f"Transcription job {job_name} is {job_status}. Polling again in {poll_interval_seconds} seconds...")
        time.sleep(poll_interval_seconds)

    return TranscriptionJobResult(job_name=job_name, status="TIMEOUT", failure_reason="Job timed out")

if __name__ == '__main__':
    # Replace with an actual job name to poll
    job_to_poll = "my-batch-transcription-job-1"
    print(f"Polling transcription job: {job_to_poll}")
    result = poll_transcription_job(job_to_poll)

    if result.status == "COMPLETED":
        print(f"Job {result.job_name} completed. Transcript URI: {result.transcript_file_uri}")
    elif result.status == "FAILED":
        print(f"Job {result.job_name} failed. Reason: {result.failure_reason}")
    elif result.status == "TIMEOUT":
        print(f"Job {result.job_name} timed out. Reason: {result.failure_reason}")
    else:
        print(f"Job {result.job_name} status: {result.status}")
