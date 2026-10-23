import boto3

def create_cloudwatch_client():
    return boto3.client('cloudwatch')