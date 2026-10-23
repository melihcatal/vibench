import os
import boto3
from speech_client import get_speech_client


def submit_transcription(audio_file_path, job_name=None):
    """Submit an audio file for batch transcription using Amazon Transcribe.

    Parameters
    ----------
    audio_file_path : str
        Path to the audio file to transcribe.
    job_name : str, optional
        Optional job name to identify the transcription job.

    Returns
    -------
    str
        The name of the created transcription job.
    """
    client = get_speech_client("boto3")
    # Ensure required credentials are present
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not (aws_key and aws_secret):
        raise RuntimeError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set")
    # Configure client (region can be set via environment or default)
    transcribe = client
    if job_name is None:
        job_name = f"transcribe-{os.path.basename(audio_file_path).split(',')[0]}-{int(time.time())}"
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={
            "MediaFileUri": f"s3://{os.getenv('AWS_S3_BUCKET__STT__INPUTS')}/{os.path.basename(audio_file_path)}"
        },
        MediaFormat="wav",  # adjust based on your file format
        LanguageCode="en-US",
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]
