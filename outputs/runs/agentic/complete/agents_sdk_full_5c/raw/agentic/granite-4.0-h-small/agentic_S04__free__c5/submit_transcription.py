import os
from speech_client import BatchSpeechClient
from speech_models import TranscriptionJobRequest

PROJECT_ID = os.getenv('BATCH_SPEECH_PROJECT_ID')
LOCATION = os.getenv('BATCH_SPEECH_LOCATION', 'us-central1')
MODEL_ID = os.getenv('BATCH_SPEECH_MODEL_ID', 'en-US-Transcribe')

def submit_transcription(audio_file_path: str, job_id: str) -> str:
    client = BatchSpeechClient()
    payload = TranscriptionJobRequest(
        audio_uri=f'gs://{os.getenv(''BATCH_SPEECH_BUCKET'')}/{audio_file_path}',
        model=MODEL_ID,
        job_id=job_id,
        enable_diarization=False,
        enable_timestamps=False
    )
    response = client.create_transcription_job(request=payload, location=LOCATION, project=PROJECT_ID)
    return response.job_id
