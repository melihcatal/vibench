import time
from speech_client import SpeechClient
from speech_models import TranscriptionResult

def poll_transcription(job_name: str, wait_interval: int = 5) -> TranscriptionResult:
    client = SpeechClient().get_client()
    while True:
        try:
            response = client.get_transcription_job(TranscriptionJobName=job_name)
            job_status = response['TranscriptionJob']['TranscriptionJobStatus']

            if job_status == 'COMPLETED':
                transcript_file_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
                # In a real scenario, you'd download and parse the transcript from this URI.
                # For simplicity, we'll just indicate it's completed.
                return TranscriptionResult(transcript=f"Transcript available at: {transcript_file_uri}", job_status=job_status)
            elif job_status == 'FAILED':
                failure_reason = response['TranscriptionJob']['FailureReason']
                print(f"Transcription job failed: {failure_reason}")
                return TranscriptionResult(transcript="", job_status=job_status)
            else:
                print(f"Transcription job status: {job_status}. Waiting...")
                time.sleep(wait_interval)
        except client.exceptions.NotFoundException:
            print(f"Transcription job '{job_name}' not found.")
            return TranscriptionResult(transcript="", job_status="NOT_FOUND")
        except Exception as e:
            print(f"Error polling transcription job: {e}")
            return TranscriptionResult(transcript="", job_status="ERROR")

if __name__ == '__main__':
    # Example usage (requires AWS credentials)
    # Replace with an actual job name submitted via submit_transcription.py
    job_name = "my-test-transcription-job"
    result = poll_transcription(job_name)
    if result.job_status == 'COMPLETED':
        print(f"Transcription completed: {result.transcript}")
    elif result.job_status == 'FAILED':
        print("Transcription failed.")
    else:
        print("Transcription did not complete or failed to retrieve status.")
