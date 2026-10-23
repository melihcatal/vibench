import boto3

def get_observability_client():
    return boto3.client('cloudwatch')