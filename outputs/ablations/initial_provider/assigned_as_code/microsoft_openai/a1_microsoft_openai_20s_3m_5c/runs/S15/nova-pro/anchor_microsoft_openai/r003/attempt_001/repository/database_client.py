import boto3

def create_dynamodb_client(region_name=None):
    return boto3.client('dynamodb', region_name=region_name)

def create_dynamodb_resource(region_name=None):
    return boto3.resource('dynamodb', region_name=region_name)