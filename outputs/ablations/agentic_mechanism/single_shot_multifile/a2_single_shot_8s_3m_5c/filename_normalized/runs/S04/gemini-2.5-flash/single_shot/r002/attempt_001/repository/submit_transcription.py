import os
import boto3
from speech_client import get_aws_transcribe_client
from speech_models import TranscriptionJobRequest, TranscriptionJobStatus

def submit_transcription_job(request: TranscriptionJobRequest) -> TranscriptionJobStatus:
    transcribe_client = get_aws_transcribe_client()

    job_settings = {}
    if request.enable_speaker_diarization:
        job_settings["SpeakerDiarization"] = {
            "EnableSpeakerDiarization": True,
            "MaxSpeakerLabels": request.max_speakers
        }
    
    # AWS Transcribe typically outputs word-level timestamps by default, if we parse the full JSON. No special 'setting' needed here.
    # Output location is defined by OutputBucketName and OutputKey (optional prefix).
    
    media_format = os.path.splitext(request.audio_file_uri)[1][1:] # e.g., 'mp3', 'flac'
    if not media_format: # Default if no extension
        media_format = 'mp3'

    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=request.job_name,
        Media={
            "MediaFileUri": request.audio_file_uri
        },
        MediaFormat=media_format,
        LanguageCode=request.language_code,
        OutputBucketName=request.output_bucket_name,
        Settings=job_settings
    )

    job_status = response["TranscriptionJob"]
    return TranscriptionJobStatus(
        job_name=job_status["TranscriptionJobName"],
        status=job_status["TranscriptionJobStatus"]
    )
