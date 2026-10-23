import requests
from speech_client import get_transcribe_client

def poll_transcription(job_name: str):
    transcribe_client = get_transcribe_client()
    response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    job_status = response['TranscriptionJob']['TranscriptionJobStatus']

    if job_status == 'COMPLETED':
        transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcript_content = requests.get(transcript_uri).text
        return {'status': job_status, 'transcript': transcript_content}
    else:
        return {'status': job_status}
