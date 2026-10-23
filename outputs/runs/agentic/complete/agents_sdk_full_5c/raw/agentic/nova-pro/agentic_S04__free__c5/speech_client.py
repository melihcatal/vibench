import boto3

transcribe = boto3.client('transcribe')

def create_transcribe_client():
    return transcribe