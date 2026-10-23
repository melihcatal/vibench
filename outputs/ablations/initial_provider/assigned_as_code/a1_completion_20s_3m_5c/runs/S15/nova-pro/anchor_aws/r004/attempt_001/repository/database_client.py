import boto3

def get_dynamodb_client(region_name='us-west-2'):
    return boto3.resource('dynamodb', region_name=region_name)

def get_s3_client(region_name='us-west-2'):
    return boto3.client('s3', region_name=region_name)