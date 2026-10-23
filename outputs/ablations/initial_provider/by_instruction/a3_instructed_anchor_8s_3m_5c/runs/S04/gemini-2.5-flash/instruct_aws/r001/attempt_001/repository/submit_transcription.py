from speech_client import get_transcribe_client
from speech_models import TranscriptionRequest
import os

def submit_transcription_job(request: TranscriptionRequest) -> str:
    transcribe_client = get_transcribe_client()
    job_name = request.job_name if request.job_name else f"transcription-job-{os.urandom(4).hex()}"
    
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': request.audio_file_uri},
        MediaFormat='mp3', # Assuming mp3 for example, can be dynamic
        LanguageCode=request.language_code
    )
    return response['TranscriptionJob']['TranscriptionJobName']
