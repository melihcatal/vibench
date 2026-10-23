import boto3
import os

def get_bedrock_client(service_name, region_name=None):
    region = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client(service_name, region_name=region)

def get_model_config(model_id=None):
    # In a real application, this might load from a config file or database
    # For this example, we'll use a simple dictionary.
    config = {
        "model_id": model_id or os.environ.get("BEDROCK_MODEL_ID", "us.amazon.nova-pro-v1:0"),
        "region": os.environ.get("AWS_REGION", "us-east-1"),
        "max_tokens": 512,
        "temperature": 0.5,
    }
    return config
