import boto3
import json

def generate_spoken_brief(text):
    client = boto3.client('polly')
    response = client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    with open('spoken_brief.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())