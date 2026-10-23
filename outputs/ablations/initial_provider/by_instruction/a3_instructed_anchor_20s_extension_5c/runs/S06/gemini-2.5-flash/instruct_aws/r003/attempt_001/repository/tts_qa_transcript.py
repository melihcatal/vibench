import boto3
import os
import time
from botocore.exceptions import ClientError

def tts_qa_transcript(audio_file_uri: str, job_name: str, media_format: str = "mp3", language_code: str = "en-US") -> str:
    """
    Transcribes synthesized QA samples using AWS Transcribe.

    Args:
        audio_file_uri: The S3 URI of the audio file to transcribe (e.g., "s3://your-bucket/your-audio-file.mp3").
        job_name: A unique name for the transcription job.
        media_format: The format of the audio file (e.g., "mp3", "wav").
        language_code: The language code of the audio (e.g., "en-US").

    Returns:
        The transcribed text.
    """
    transcribe_client = boto3.client(
        "transcribe",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    try:
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': audio_file_uri},
            MediaFormat=media_format,
            LanguageCode=language_code
        )

        while True:
            status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            if status["TranscriptionJob"]["TranscriptionJobStatus"] in ["COMPLETED", "FAILED"]:
                break
            time.sleep(5)

        if status["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
            transcript_file_uri = status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            # In a real scenario, you would fetch this URI and parse the JSON to get the transcript.
            # For simplicity, we'll return a placeholder or an indication that it's completed.
            return f"Transcription completed. Transcript available at: {transcript_file_uri}"
        else:
            return f"Transcription failed: {status['TranscriptionJob']['FailureReason']}"

    except ClientError as e:
        return f"AWS Transcribe error: {e}"
