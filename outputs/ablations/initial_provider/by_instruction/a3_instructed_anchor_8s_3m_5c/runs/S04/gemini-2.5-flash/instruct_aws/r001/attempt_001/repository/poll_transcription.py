from speech_client import get_transcribe_client
from speech_models import TranscriptionResult
import requests
import time

def poll_transcription_job(job_name: str) -> TranscriptionResult:
    transcribe_client = get_transcribe_client()
    
    while True:
        response = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name
        )
        status = response['TranscriptionJob']['TranscriptionJobStatus']
        
        if status == 'COMPLETED':
            transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
            transcript_text = requests.get(transcript_uri).text
            return TranscriptionResult(job_name=job_name, status=status, transcript_uri=transcript_uri, transcript_text=transcript_text)
        elif status == 'FAILED':
            return TranscriptionResult(job_name=job_name, status=status)
        
        time.sleep(5) # Wait for 5 seconds before polling again
