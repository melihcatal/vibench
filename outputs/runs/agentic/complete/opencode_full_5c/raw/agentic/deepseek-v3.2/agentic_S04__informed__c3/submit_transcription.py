import os
import boto3
from botocore.exceptions import ClientError
from speech_client import get_speech_client
from speech_models import TranscriptionRequest


def submit_transcription(audio_file_path: str, language_code: str = "en-US") -> str:
    """
    Submit an audio file for batch transcription using Amazon Transcribe.

    Args:
        audio_file_path: Path to the audio file
        language_code: Language code for transcription (default: en-US)

    Returns:
        Transcription job ID
    """
    client = get_speech_client()

    # Generate a unique job name
    import uuid

    job_name = f"transcription-job-{uuid.uuid4().hex[:8]}"

    # Upload audio file to S3 first (required for batch transcription)
    s3_client = boto3.client("s3")
    bucket_name = os.environ.get("AWS_TRANSCRIBE_BUCKET", "transcription-audio-bucket")

    try:
        # Upload to S3
        s3_key = f"audio/{job_name}.wav"
        s3_client.upload_file(audio_file_path, bucket_name, s3_key)

        # Start transcription job
        response = client.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode=language_code,
            MediaFormat="wav",
            Media={"MediaFileUri": f"s3://{bucket_name}/{s3_key}"},
            Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": 10},
        )

        job_id = response["TranscriptionJob"]["TranscriptionJobName"]
        print(f"Submitted transcription job: {job_id}")
        return job_id

    except ClientError as e:
        print(f"Error submitting transcription: {e}")
        raise


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        job_id = submit_transcription(sys.argv[1])
        print(f"Job ID: {job_id}")
    else:
        print("Usage: python submit_transcription.py <audio_file_path>")
