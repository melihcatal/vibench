import os
import boto3
from speech_models import AudioFormat

def transcribe_sample(audio_bytes: bytes, audio_format: AudioFormat = "mp3") -> str:
    """Transcribe synthesized QA audio using Amazon Transcribe.

    Requires AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
    """
    transcribe = boto3.client(
        "transcribe",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    # Upload audio to a temporary S3 bucket (placeholder)
    s3 = boto3.client(
        "s3",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    bucket = "temp-tts-transcripts"
    key = f"sample.{audio_format}"
    s3.put_object(Bucket=bucket, Key=key, Body=audio_bytes)
    # Submit transcription job
    transcribe.start_transcription_job(
        TranscriptionJobName="qa-sample-job",
        Media={"MediaFileUri": f"https://{bucket}.s3.amazonaws.com/{key}"},
        MediaFormat=audio_format,
        LanguageCode="en-US",
    )
    # Poll until complete (simplified)
    while True:
        job = transcribe.get_transcription_job(TranscriptionJobName="qa-sample-job")
        status = job["TranscriptionJob"]["TranscriptionJobStatus"]
        if status != "IN_PROGRESS":
            break
    transcript = job["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    # Simple fetch of transcript (placeholder)
    s3_response = s3.get_object(Bucket=bucket, Key=transcript)
    return s3_response["Body"].read().decode()