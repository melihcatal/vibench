import boto3

def get_cloudwatch_client():
    return boto3.client('cloudwatch')