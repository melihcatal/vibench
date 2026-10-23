import boto3


def get_bedrock_client(config):
    region = config.get('region', 'us-east-1')
    return boto3.client('bedrock-runtime', region_name=region)