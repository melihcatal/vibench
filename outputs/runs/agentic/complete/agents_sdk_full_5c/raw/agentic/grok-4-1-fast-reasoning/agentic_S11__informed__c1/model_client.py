import boto3

def get_bedrock_runtime_client(region: str = 'us-east-1'):
    return boto3.client('bedrock-runtime', region_name=region)

def get_bedrock_client(region: str = 'us-east-1'):
    return boto3.client('bedrock', region_name=region)
