import boto3

def get_dynamodb_client(region_name=None):
    return boto3.client('dynamodb', region_name=region_name)

def get_dynamodb_resource(region_name=None):
    return boto3.resource('dynamodb', region_name=region_name)