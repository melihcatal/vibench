import boto3
import os

def select_platform_resource(model_family_hint: str) -> str:
    client = boto3.client(
        'bedrock-runtime',
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    response = client.list_foundation_models()
    model_summaries = response['modelSummaries']
    for summary in model_summaries:
        model_id = summary['modelId']
        if model_family_hint.lower() in model_id.lower():
            return model_id
    raise ValueError(f'No matching model found for hint: {model_family_hint}')