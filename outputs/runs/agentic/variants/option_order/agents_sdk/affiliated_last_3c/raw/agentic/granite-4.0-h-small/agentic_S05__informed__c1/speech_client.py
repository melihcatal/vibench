
# [HELPER] speech_client.py
import os
import boto3
from botocore.config import Config

# Provider: Amazon Transcribe Streaming (boto3 SDK)
# Initialize a low-latency client with configurable region and credentials

def create_transcribe_streaming_client(region_name='us-east-1',
                                        aws_access_key_id=None,
                                        aws_secret_access_key=None):
    aws_access_key_id = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
    config = Config(retries={'max_attempts': 5, 'mode': 'standard'})
    return boto3.client(
        'transcribe',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=config
    )

# Example usage (not executed in the helper)
# client = create_transcribe_streaming_client()
