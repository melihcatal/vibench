import os
import boto3

client = boto3.client('polly', region_name='us-west-2', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def generate_speech(text):
    response = client.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
    with open('speech.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())