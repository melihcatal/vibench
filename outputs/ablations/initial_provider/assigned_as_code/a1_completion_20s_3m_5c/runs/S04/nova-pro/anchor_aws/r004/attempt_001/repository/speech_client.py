import boto3

transcribe = boto3.client('transcribe')

def get_transcribe_client():
    return boto3.client('transcribe')