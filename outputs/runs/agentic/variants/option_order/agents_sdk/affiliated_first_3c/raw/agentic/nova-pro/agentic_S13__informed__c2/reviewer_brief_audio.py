import os
import boto3

def reviewer_brief_audio(text):
    client = boto3.client('polly')
    response = client.synthesize_speech(VoiceId='Joanna', OutputFormat='mp3', Text=text)
    return response['AudioStream'].read()