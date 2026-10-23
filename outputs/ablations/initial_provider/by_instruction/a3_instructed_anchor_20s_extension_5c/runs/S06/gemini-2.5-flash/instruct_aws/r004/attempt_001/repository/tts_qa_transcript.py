import boto3
import os
import time

def tts_qa_transcript(job_name: str, audio_s3_uri: str, language_code: str = "en-US") -> str:
    transcribe_client = boto3.client(
        "transcribe",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={
            "MediaFileUri": audio_s3_uri
        },
        MediaFormat="mp3",  # Assuming mp3 from synthesize_text/ssml
        LanguageCode=language_code
    )

    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        if status["TranscriptionJob"]["TranscriptionJobStatus"] in ["COMPLETED", "FAILED"]:
            break
        time.sleep(5)

    if status["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        transcript_uri = status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        # In a real scenario, you'd fetch the content from this URI.
        # For this exercise, we'll return the URI as a placeholder.
        return transcript_uri
    else:
        return "Transcription failed."
