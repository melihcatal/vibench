import os
import boto3

# Configuration for AWS Bedrock
AWS_REGION = 'us-west-2'

# Initialize the Bedrock client
bedrock_client = boto3.client('bedrock-runtime', region_name=AWS_REGION)


def select_model_family(model_family):
    """Select a specific model family from AWS Bedrock."""
    if model_family == 'anthropic':
        return 'anthropic.claude-v2'
    elif model_family == 'amazon':
        return 'amazon.titan-text-express-v1'
    else:
        raise ValueError('Unsupported model family')


def perform_inference(model_family, prompt):
    """Perform inference using the selected model family."""
    model_id = select_model_family(model_family)
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body={
            'prompt': prompt,
            'max_tokens': 150
        }
    )
    return response['body']['outputs'][0]['text']