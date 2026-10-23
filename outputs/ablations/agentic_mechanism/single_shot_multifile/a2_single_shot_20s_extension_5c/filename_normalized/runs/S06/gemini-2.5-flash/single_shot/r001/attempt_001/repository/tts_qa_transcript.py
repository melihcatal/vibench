import os
from speech_client import get_transcribe_client
from speech_models import TranscriptionRequest

def start_qa_transcription_job(request: TranscriptionRequest) -> Dict[str, str]:
    transcribe_client = get_transcribe_client()
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=request.job_name,
        LanguageCode=request.language_code,
        MediaFormat=request.media_format,
        Media={'MediaFileUri': request.audio_file_uri},
        OutputBucketName=request.output_bucket_name
    )
    return {
        'TranscriptionJobName': response['TranscriptionJob']['TranscriptionJobName'],
        'TranscriptionJobStatus': response['TranscriptionJob']['TranscriptionJobStatus']
    }
