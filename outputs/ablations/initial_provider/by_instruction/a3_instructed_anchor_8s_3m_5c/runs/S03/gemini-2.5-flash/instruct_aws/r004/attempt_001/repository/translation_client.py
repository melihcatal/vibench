import boto3

def get_aws_translate_client():
    """
    Returns an AWS Translate client.
    """
    return boto3.client('translate')
