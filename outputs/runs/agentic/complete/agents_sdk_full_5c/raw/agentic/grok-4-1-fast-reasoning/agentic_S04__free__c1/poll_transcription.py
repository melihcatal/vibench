import time
from speech_client import get_speech_client

def poll_transcription(job_id: str) -> str:
    client = get_speech_client()
    transcript = client.transcripts.get(job_id)
    while transcript.status not in ['completed', 'error']:
        time.sleep(10)
        transcript = client.transcripts.get(job_id)
    if transcript.status == 'error':
        raise ValueError(f'Transcription error: {transcript.error}')
    return transcript.text