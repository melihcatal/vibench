from speech_client import get_transcribe_client
from speech_models import DiarizationRequest, TranscriptionResult
import os

def request_diarized_transcript(request: DiarizationRequest) -> str:
    transcribe_client = get_transcribe_client()
    job_name = request.job_name if request.job_name else f"diarization-job-{os.urandom(4).hex()}"

    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': request.audio_file_uri},
        MediaFormat='mp3',
        LanguageCode=request.language_code,
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 2 # Example: allow up to 2 speakers
        }
    )
    return response['TranscriptionJob']['TranscriptionJobName']
