import boto3
import os

def submit_aws_transcription_job(audio_file_uri: str, job_name: str, language_code: str = "en-US"):
    """
    Submits an audio file to AWS S3 and starts a Transcribe transcription job.
    """
    s3_bucket = os.environ.get("AWS_S3_BUCKET_NAME")
    if not s3_bucket:
        raise ValueError("AWS_S3_BUCKET_NAME environment variable not set.")

    # In a real scenario, you would upload the audio file to S3 first
    # For this example, we assume audio_file_uri is already an S3 URI.

    transcribe_client = boto3.client("transcribe", region_name=os.environ.get("AWS_REGION", "us-east-1"))

    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': audio_file_uri},
        MediaFormat='mp3',  # Assuming mp3, could be dynamic
        LanguageCode=language_code
    )
    return response['TranscriptionJob']
