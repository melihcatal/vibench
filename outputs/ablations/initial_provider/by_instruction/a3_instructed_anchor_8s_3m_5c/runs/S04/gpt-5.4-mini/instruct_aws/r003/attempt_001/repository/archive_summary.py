import os

import boto3


def archive_summary(text: str) -> dict:
    client = boto3.client('bedrock-runtime', region_name=os.getenv('AWS_REGION', os.getenv('AWS_DEFAULT_REGION', 'us-east-1')))
    response = client.invoke_model(modelId='anthropic.claude-3-haiku-20240307-v1:0', body=text.encode('utf-8'), contentType='text/plain', accept='application/json')
    return {'modelId': 'anthropic.claude-3-haiku-20240307-v1:0', 'response': response}
