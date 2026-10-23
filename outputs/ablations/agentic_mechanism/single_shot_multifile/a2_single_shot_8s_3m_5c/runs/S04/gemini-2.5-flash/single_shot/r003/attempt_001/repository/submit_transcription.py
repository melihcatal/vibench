import os
from speech_client import get_transcribe_client
from speech_models import TranscriptionJobRequest

def submit_transcription(request: TranscriptionJobRequest) -> str:
    """
    Submits an audio file for batch transcription using AWS Transcribe.
    Returns the job name.
    """
    transcribe_client = get_transcribe_client()
    
    job_settings = {
        "LanguageCode": request.language_code
    }
    
    if request.output_bucket:
        job_settings["OutputBucketName"] = request.output_bucket

    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=request.job_name,
        Media={
            "MediaFileUri": request.media_uri
        },
        **job_settings
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]
