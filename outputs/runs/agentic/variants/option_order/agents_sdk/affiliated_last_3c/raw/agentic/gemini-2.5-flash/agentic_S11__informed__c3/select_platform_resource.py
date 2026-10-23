import boto3
import os

def list_bedrock_foundation_models(inference_type: str = "TEXT"):
    """
    Lists available Amazon Bedrock foundation models filtered by inference type.
    """
    client = boto3.client(
        "bedrock",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    
    response = client.list_foundation_models(
        byInferenceType=inference_type
    )
    
    model_summaries = response.get('modelSummaries', [])
    return [model['modelId'] for model in model_summaries if model.get('modelId')]

def get_default_text_model_id():
    """
    Returns a common default text model ID for Bedrock.
    """
    return "anthropic.claude-v2"
