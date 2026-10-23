import boto3


def speech_client(region, api_key, secret_key):
    return boto3.client('transcribe', region_name=region, aws_access_key_id=api_key, aws_secret_access_key=secret_key)