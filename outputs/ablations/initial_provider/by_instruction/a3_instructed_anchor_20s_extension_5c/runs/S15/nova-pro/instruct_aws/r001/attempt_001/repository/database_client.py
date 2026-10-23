import boto3

def get_dynamodb_client():
    return boto3.client('dynamodb')

def get_dynamodb_resource():
    return boto3.resource('dynamodb')