import os
import boto3

def generate_briefing(text):
    polly = boto3.client('polly', region_name='us-west-2')
    response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
    return response['AudioStream'].read()
