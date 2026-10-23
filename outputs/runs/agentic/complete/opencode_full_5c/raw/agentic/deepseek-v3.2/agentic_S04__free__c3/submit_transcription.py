import os
import boto3
from botocore.exceptions import ClientError
from speech_client import get_speech_client
from speech_models import TranscriptionRequest, TranscriptionJob


def submit_transcription(
    audio_file_path: str, language_code: str = "en-US"
) -> TranscriptionJob:
    """
    Submit an audio file for batch transcription using AWS Transcribe.

    Args:
        audio_file_path: Path to the audio file
        language_code: Language code for transcription (default: en-US)

    Returns:
        TranscriptionJob object with job details
    """
    client = get_speech_client()

    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    job_name = (
        f"transcription_{os.path.basename(audio_file_path)}_{os.urandom(4).hex()}"
    )

    try:
        response = client.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode=language_code,
            MediaFormat=audio_file_path.split(".")[-1].lower(),
            Media={
                "MediaFileUri": f"s3://transcription-audio-bucket/{os.path.basename(audio_file_path)}"
            },
            Settings={
                "ShowSpeakerLabels": True,
                "MaxSpeakerLabels": 10,
                "ChannelIdentification": False,
            },
        )

        job = response["TranscriptionJob"]
        return TranscriptionJob(
            job_id=job["TranscriptionJobName"],
            status=job["TranscriptionJobStatus"],
            language_code=language_code,
            audio_file=audio_file_path,
            created_at=job.get("CreationTime"),
            transcript_uri=job.get("Transcript", {}).get("TranscriptFileUri"),
        )

    except ClientError as e:
        raise Exception(f"AWS Transcribe error: {e.response['Error']['Message']}")
