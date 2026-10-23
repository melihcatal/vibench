import boto3

def get_dynamodb_client(region_name, aws_access_key_id, aws_secret_access_key):
    return boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)