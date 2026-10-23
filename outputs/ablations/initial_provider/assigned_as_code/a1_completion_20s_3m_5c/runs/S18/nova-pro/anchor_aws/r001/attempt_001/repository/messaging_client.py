import boto3

def get_sns_client(region):
    return boto3.client('sns', region_name=region)

def get_sqs_client(region):
    return boto3.client('sqs', region_name=region)