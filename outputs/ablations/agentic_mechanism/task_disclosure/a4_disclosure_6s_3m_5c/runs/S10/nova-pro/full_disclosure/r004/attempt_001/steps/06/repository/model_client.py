import os

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

BEDROCK_REGION = 'us-east-1'
BEDROCK_MODEL_ID = 'amazon.titan-text-express-v1'

def create_bedrock_client():
    try:
        client = boto3.client('bedrock-runtime', region_name=BEDROCK_REGION)
        return client
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise Exception('AWS credentials not found or incomplete') from e

def select_model(model_id=BEDROCK_MODEL_ID):
    if model_id not in ['amazon.titan-text-express-v1', 'amazon.titan-text-lite-v1']:
        raise ValueError('Unsupported model ID')
    return model_id

if __name__ == '__main__':
    client = create_bedrock_client()
    print(f'Bedrock client created for region: {BEDROCK_REGION}')
    model = select_model()
    print(f'Selected model: {model}')