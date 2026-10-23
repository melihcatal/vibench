import os
import boto3
from gtts import gTTS

def generate_audio_brief(brief_text: str, output_path: str = 'moderation_brief.mp3'):
    """Create an MP3 spoken brief using Google Text‑to‑Speech and save it locally."""
    tts = gTTS(text=brief_text, lang='en')
    tts.save(output_path)
    return output_path

# Example provider configuration (AWS S3) for uploading the brief
s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-1'))

def upload_brief_to_s3(local_path: str, bucket_name: str, object_key: str):
    """Upload the generated audio file to an S3 bucket."""
    s3.upload_file(local_path, bucket_name, object_key)
