import os
import boto3

def generate_speech(text):
    polly = boto3.client('polly', region_name='us-west-2')
    response = polly.synthesize_speech(
        VoiceId='Joanna',
        OutputFormat='mp3',
        Text=text
    )
    with open('speech.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
