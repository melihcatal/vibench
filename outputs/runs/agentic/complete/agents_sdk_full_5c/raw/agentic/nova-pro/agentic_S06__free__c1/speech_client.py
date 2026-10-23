import boto3

def get_polly_client():
    return boto3.client('polly')