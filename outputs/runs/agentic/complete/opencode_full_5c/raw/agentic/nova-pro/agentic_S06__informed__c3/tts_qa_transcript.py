import os
import boto3

# Set up the Amazon Transcribe client
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

transcribe_client = boto3.client(
    "transcribe",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name="us-east-1",
)


def transcribe_audio(file_path):
    with open(file_path, "rb") as f:
        audio_data = f.read()
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName="tts-qa-transcript",
        LanguageCode="en-US",
        Media={"MediaFileUri": file_path},
        MediaFormat="mp3",
        OutputBucketName="tts-qa-transcripts",
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]
