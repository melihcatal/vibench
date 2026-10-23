import boto3

def get_speech_client():
    return boto3.client('transcribe', region_name='us-west-2')