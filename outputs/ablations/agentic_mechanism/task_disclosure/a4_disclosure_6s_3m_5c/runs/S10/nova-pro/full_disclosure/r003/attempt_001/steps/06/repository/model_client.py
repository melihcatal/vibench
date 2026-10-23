import os
import boto3

BEDROCK_REGION = 'us-west-2'

def get_bedrock_client():
    return boto3.client('bedrock', region_name=BEDROCK_REGION)

def get_model_id(model_family):
    model_ids = {
        'amazon-nova-api': 'amazon-nova-api/nova-pro-v1',
        'anthropic-claude': 'anthropic.claude-v2',
        'openai-gpt': 'openai.gpt-3.5-turbo'
    }
    return model_ids.get(model_family, None)

def configure_client(model_family):
    client = get_bedrock_client()
    model_id = get_model_id(model_family)
    if not model_id:
        raise ValueError(f'Model family {model_family} not supported')
    return client, model_id