import boto3

def get_bedrock_runtime_client(region_name="us-east-1"):
    """Provides a configured boto3 client for AWS Bedrock Runtime."""
    return boto3.client("bedrock-runtime", region_name=region_name)

def get_comprehend_client(region_name="us-east-1"):
    """Provides a configured boto3 client for AWS Comprehend."""
    return boto3.client("comprehend", region_name=region_name)

def get_translate_client(region_name="us-east-1"):
    """Provides a configured boto3 client for AWS Translate."""
    return boto3.client("translate", region_name=region_name)

def get_polly_client(region_name="us-east-1"):
    """Provides a configured boto3 client for AWS Polly."""
    return boto3.client("polly", region_name=region_name)
