import os
import boto3

polly_client = boto3.client('polly', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def synthesize_text(text):
    response = polly_client.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
    return response['AudioStream'].read()