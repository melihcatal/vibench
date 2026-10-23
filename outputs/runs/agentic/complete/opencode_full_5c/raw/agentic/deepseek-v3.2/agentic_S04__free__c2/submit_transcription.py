import os
import boto3
from botocore.exceptions import ClientError
from speech_client import get_speech_client
from speech_models import TranscriptionRequest


def submit_transcription(audio_file_path: str, language_code: str = "en-US") -> str:
    """
    Submit an audio file for batch transcription using AWS Transcribe.

    Args:
        audio_file_path: Path to the audio file to transcribe
        language_code: Language code for the audio (default: en-US)

    Returns:
        Transcription job ID
    """
    client = get_speech_client()

    # Upload audio file to S3 first (required for AWS Transcribe)
    s3_client = boto3.client("s3")
    bucket_name = os.environ.get("AWS_TRANSCRIBE_BUCKET", "transcription-audio-bucket")

    # Generate a unique key for the audio file
    import uuid

    audio_key = f"audio/{uuid.uuid4()}_{os.path.basename(audio_file_path)}"

    try:
        # Upload audio to S3
        s3_client.upload_file(audio_file_path, bucket_name, audio_key)

        # Create transcription job
        job_name = f"transcription-job-{uuid.uuid4()}"
        media_uri = f"s3://{bucket_name}/{audio_key}"

        response = client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": media_uri},
            MediaFormat=audio_file_path.split(".")[-1].lower(),
            LanguageCode=language_code,
            Settings={
                "ShowSpeakerLabels": True,
                "MaxSpeakerLabels": 10,
                "ChannelIdentification": False,
            },
        )

        job_id = response["TranscriptionJob"]["TranscriptionJobName"]
        print(f"Transcription job submitted: {job_id}")
        return job_id

    except ClientError as e:
        print(f"Error submitting transcription: {e}")
        raise
