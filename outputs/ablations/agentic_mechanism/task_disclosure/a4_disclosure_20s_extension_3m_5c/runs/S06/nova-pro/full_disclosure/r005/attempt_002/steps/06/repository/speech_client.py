import os
import boto3

def get_polly_client():
    return boto3.client('polly',
                        region_name='us-west-2',
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def synthesize_speech(text, voice_id, output_format='mp3'):
    polly_client = get_polly_client()
    response = polly_client.synthesize_speech(Text=text,
                                              VoiceId=voice_id,
                                              OutputFormat=output_format)
    return response['AudioStream'].read()