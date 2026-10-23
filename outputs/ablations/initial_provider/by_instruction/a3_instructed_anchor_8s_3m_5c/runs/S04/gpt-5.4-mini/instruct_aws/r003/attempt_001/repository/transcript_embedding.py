import os

import boto3


def transcript_embedding(text: str) -> dict:
    client = boto3.client('bedrock-runtime', region_name=os.getenv('AWS_REGION', os.getenv('AWS_DEFAULT_REGION', 'us-east-1')))
    response = client.invoke_model(modelId='amazon.titan-embed-text-v2:0', body=text.encode('utf-8'), contentType='text/plain', accept='application/json')
    return {'modelId': 'amazon.titan-embed-text-v2:0', 'response': response}
