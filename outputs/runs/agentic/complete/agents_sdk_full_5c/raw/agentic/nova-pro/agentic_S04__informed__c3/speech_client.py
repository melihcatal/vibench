import boto3

def create_transcribe_client():
    return boto3.client('transcribe')

def create_translate_client():
    return boto3.client('translate')