# Amazon Transcribe integration
import os
import boto3

TRANSCRIBE = boto3.client(
    "transcribe",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def submit_transcription(job_name, audio_file_path, language_code="en-US"):
    """Submit an audio file for batch transcription using Amazon Transcribe. Returns the job name for later polling."""
    TRANSCRIBE.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": f"s3://{os.getenv('S3_BUCKET')}/{audio_file_path}"},
        MediaFormat="mp3",  # adjust as needed
        LanguageCode=language_code,
        Settings={"VocabularyName": os.getenv("TRANSCRIBE_VOCABULARY_NAME", None)},
    )
    return job_name
