import boto3

def create_cloudwatch_client():
    return boto3.client('cloudwatch')

def create_translate_client():
    return boto3.client('translate')

def create_s3_client():
    return boto3.client('s3')