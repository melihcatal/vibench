import boto3
import os


def get_speech_client(config=None):
    config = config or {}
    region = config.get('region', os.getenv('AWS_REGION'))
    aws_access_key_id = config.get('aws_access_key_id', os.getenv('AWS_ACCESS_KEY_ID'))
    aws_secret_access_key = config.get('aws_secret_access_key', os.getenv('AWS_SECRET_ACCESS_KEY'))
    client = boto3.client(
        'transcribe',
        region_name=region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    return client