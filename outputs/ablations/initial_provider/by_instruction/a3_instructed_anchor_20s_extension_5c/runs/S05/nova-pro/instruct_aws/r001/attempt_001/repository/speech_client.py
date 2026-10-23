import boto3

def get_speech_client():
    return boto3.client('transcribestreaming')