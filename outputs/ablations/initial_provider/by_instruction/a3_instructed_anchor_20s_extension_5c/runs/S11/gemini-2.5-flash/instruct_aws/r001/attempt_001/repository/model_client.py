import boto3

def get_bedrock_client():
    """
    Provides a configured boto3 client for AWS Bedrock.
    Assumes AWS credentials and region are configured via environment variables
    or AWS CLI configuration.
    """
    return boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

def get_bedrock_agent_client():
    """
    Provides a configured boto3 client for AWS Bedrock Agent (for Guardrails).
    """
    return boto3.client(service_name="bedrock-agent-runtime", region_name="us-east-1")

def get_translate_client():
    """
    Provides a configured boto3 client for AWS Translate.
    """
    return boto3.client(service_name="translate", region_name="us-east-1")

def get_polly_client():
    """
    Provides a configured boto3 client for AWS Polly.
    """
    return boto3.client(service_name="polly", region_name="us-east-1")

def get_rekognition_client():
    """
    Provides a configured boto3 client for AWS Rekognition (for potential image safety checks).
    """
    return boto3.client(service_name="rekognition", region_name="us-east-1")
