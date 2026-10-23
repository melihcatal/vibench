import boto3

def get_cloudwatch_client():
    return boto3.client('cloudwatch')

def get_comprehend_client():
    return boto3.client('comprehend')

def get_translate_client():
    return boto3.client('translate')

def get_s3_client():
    return boto3.client('s3')