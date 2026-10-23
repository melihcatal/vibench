import os
import boto3

polly_client = boto3.client('polly', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def save_audio(audio_stream, file_path):
    with open(file_path, 'wb') as file:
        file.write(audio_stream)