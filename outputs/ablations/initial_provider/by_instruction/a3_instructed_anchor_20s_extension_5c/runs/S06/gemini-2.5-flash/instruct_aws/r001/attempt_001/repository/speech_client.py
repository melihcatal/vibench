import boto3

def get_polly_client():
    """
    Returns an AWS Polly client.
    """
    return boto3.client("polly", region_name="us-east-1") # AWS provider-specific region
