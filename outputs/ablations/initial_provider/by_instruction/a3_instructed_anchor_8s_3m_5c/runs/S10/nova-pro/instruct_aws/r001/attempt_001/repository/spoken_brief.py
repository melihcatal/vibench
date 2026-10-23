import boto3
import json

def generate_spoken_brief(text):
    client = boto3.client('polly', region_name='us-east-1')
    response = client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    return response['AudioStream'].read()