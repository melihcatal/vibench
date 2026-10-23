import boto3
import os
from typing import Dict, Any

def get_aws_session(region_name: str = 'us-east-1') -> boto3.Session:
    """Establishes and returns an AWS session."""
    return boto3.Session(region_name=region_name)

def get_secrets_manager_client(region_name: str = 'us-east-1') -> Any:
    """Returns a Boto3 Secrets Manager client."""
    session = get_aws_session(region_name)
    return session.client('secretsmanager')

def get_sns_client(region_name: str = 'us-east-1') -> Any:
    """Returns a Boto3 SNS client."""
    session = get_aws_session(region_name)
    return session.client('sns')

def get_comprehend_client(region_name: str = 'us-east-1') -> Any:
    """Returns a Boto3 Comprehend client."""
    session = get_aws_session(region_name)
    return session.client('comprehend')

def get_bedrock_runtime_client(region_name: str = 'us-east-1') -> Any:
    """Returns a Boto3 Bedrock Runtime client."""
    session = get_aws_session(region_name)
    return session.client('bedrock-runtime')

def get_translate_client(region_name: str = 'us-east-1') -> Any:
    """Returns a Boto3 Translate client."""
    session = get_aws_session(region_name)
    return session.client('translate')

def load_aws_config() -> Dict[str, str]:
    """Loads AWS configuration from environment variables or defaults."""
    config = {
        'AWS_REGION': os.environ.get('AWS_REGION', 'us-east-1'),
        # Add other AWS specific configurations here if needed
    }
    return config
