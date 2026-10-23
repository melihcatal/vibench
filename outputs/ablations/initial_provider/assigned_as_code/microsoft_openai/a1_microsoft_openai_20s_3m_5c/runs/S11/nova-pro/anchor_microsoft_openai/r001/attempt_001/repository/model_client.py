import os

AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')

def get_bedrock_client():
    return boto3.client('bedrock-runtime', region_name=AWS_REGION)