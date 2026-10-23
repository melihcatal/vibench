import boto3
import os
import time
from typing import Dict, Any

def tts_qa_transcript(audio_s3_uri: str, job_name: str, media_format: str = "mp3", language_code: str = "en-US") -> Dict[str, Any]:
    """
    Transcribes synthesized QA samples to verify spoken output using Amazon Transcribe.

    Args:
        audio_s3_uri: The S3 URI of the audio file to transcribe (e.g., "s3://your-bucket/your-audio.mp3").
        job_name: A unique name for the transcription job.
        media_format: The format of the media file (e.g., "mp3", "wav").
        language_code: The language code of the audio (e.g., "en-US").

    Returns:
        A dictionary containing the transcription job details and result.
    """
    transcribe_client = boto3.client(
        'transcribe',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': audio_s3_uri},
        MediaFormat=media_format,
        LanguageCode=language_code
    )

    max_tries = 60
    for i in range(max_tries):
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            print(f"Job {job_name} is {job_status}.")
            break
        else:
            print(f"Waiting for {job_name}. Current status: {job_status}")
            time.sleep(5)
    else:
        print(f"Transcription job {job_name} did not complete within {max_tries} retries.")

    if job_status == 'COMPLETED':
        transcript_file_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
        return {"status": "COMPLETED", "transcript_uri": transcript_file_uri}
    else:
        return {"status": job_status, "message": job['TranscriptionJob'].get('FailureReason')}
