import boto3

def create_speech_client():
    return boto3.client('transcribe')