import boto3
import os
from typing import Optional, Dict, Any


def submit_transcription_job(
    audio_file_path: str, language_code: str = "en-US", job_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Submit an audio file for batch transcription using Amazon Transcribe.

    Args:
        audio_file_path: Path to the audio file (local or S3 URI)
        language_code: Language code for transcription (default: en-US)
        job_name: Optional custom job name

    Returns:
        Dictionary with job details including JobName and JobStatus
    """
    transcribe_client = boto3.client("transcribe")

    if job_name is None:
        import uuid

        job_name = f"transcription-job-{uuid.uuid4().hex[:8]}"

    media_format = audio_file_path.split(".")[-1].lower()
    if media_format not in ["mp3", "mp4", "wav", "flac", "ogg", "amr", "webm"]:
        media_format = "mp3"

    if audio_file_path.startswith("s3://"):
        media_uri = audio_file_path
    else:
        s3_client = boto3.client("s3")
        bucket_name = os.environ.get(
            "AWS_TRANSCRIBE_BUCKET", "transcription-audio-bucket"
        )
        object_key = f"audio/{job_name}.{media_format}"

        s3_client.upload_file(audio_file_path, bucket_name, object_key)
        media_uri = f"s3://{bucket_name}/{object_key}"

    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language_code,
        MediaFormat=media_format,
        Media={"MediaFileUri": media_uri},
        Settings={
            "ShowSpeakerLabels": True,
            "MaxSpeakerLabels": 10,
            "ChannelIdentification": False,
        },
    )

    return {
        "JobName": response["TranscriptionJob"]["TranscriptionJobName"],
        "JobStatus": response["TranscriptionJob"]["TranscriptionJobStatus"],
        "MediaUri": media_uri,
        "LanguageCode": language_code,
    }
