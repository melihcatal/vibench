import boto3
from model_client import get_bedrock_client

def select_platform_resource(model_family: str = 'anthropic.claude-3-sonnet') -> str:
    client = get_bedrock_client()
    response = client.list_foundation_models(maxResults=50)
    model_summaries = response['modelSummaries']
    for model in model_summaries:
        if model_family in model['modelId']:
            return model['modelId']
    raise ValueError(f"No model found matching {model_family}")
