import os
import boto3
from speech_client import get_aws_transcribe_client
from speech_models import TranscriptionJobRequest, TranscriptionJobStatus

def submit_diarized_transcription_job(request: TranscriptionJobRequest) -> TranscriptionJobStatus:
    transcribe_client = get_aws_transcribe_client()

    # Ensure diarization is explicitly enabled
    request.enable_speaker_diarization = True
    
    job_settings = {
        "SpeakerDiarization": {
            "EnableSpeakerDiarization": request.enable_speaker_diarization,
            "MaxSpeakerLabels": request.max_speakers
        },
        "ShowSpeakerLabels": True # Required for speaker_labels in output
    }

    media_format = os.path.splitext(request.audio_file_uri)[1][1:] 
    if not media_format:
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
