import os
import boto3

polly_client = boto3.client('polly', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def generate_speech(text):
    response = polly_client.synthesize_speech(VoiceId='Joanna', OutputFormat='mp3', Text=text)
    with open('speech.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())
