import os
from speech_client import get_transcribe_client, get_s3_client
from speech_models import TranscriptionRequest

AWS_S3_BUCKET_NAME = os.environ.get("AWS_S3_BUCKET_NAME")

def upload_audio_to_s3(file_path: str, object_name: str) -> str:
    s3_client = get_s3_client()
    try:
        s3_client.upload_file(file_path, AWS_S3_BUCKET_NAME, object_name)
        print(f"File {file_path} uploaded to s3://{AWS_S3_BUCKET_NAME}/{object_name}")
        return f"s3://{AWS_S3_BUCKET_NAME}/{object_name}"
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        raise

def submit_transcription_job(request: TranscriptionRequest):
    transcribe_client = get_transcribe_client()
    try:
        response = transcribe_client.start_transcription_job(
            TranscriptionJobName=request.job_name,
            LanguageCode=request.language_code,
            MediaFormat=request.media_format,
            Media={
                'MediaFileUri': request.media_uri
            },
            OutputBucketName=request.output_bucket,
            Settings={
                'ShowSpeakerLabels': request.show_speaker_labels,
                'MaxSpeakerLabels': request.max_speakers if request.show_speaker_labels else 0,
            }
        )
        print(f"Transcription job {request.job_name} started: {response['TranscriptionJob']['TranscriptionJobStatus']}")
        return response['TranscriptionJob']
    except Exception as e:
        print(f"Error starting transcription job: {e}")
        raise
