import boto3

def get_transcribe_client():
    return boto3.client('transcribe')

def get_s3_client():
    return boto3.client('s3')
