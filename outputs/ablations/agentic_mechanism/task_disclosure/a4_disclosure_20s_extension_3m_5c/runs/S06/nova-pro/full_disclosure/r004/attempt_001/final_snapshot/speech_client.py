import boto3

def initialize_polly_client(region_name='us-west-2'):
    return boto3.client('polly', region_name=region_name)