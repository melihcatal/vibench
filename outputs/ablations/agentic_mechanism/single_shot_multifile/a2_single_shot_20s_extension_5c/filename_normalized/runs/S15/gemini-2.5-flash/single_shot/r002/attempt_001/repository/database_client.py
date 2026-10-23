import os
import boto3

def get_dynamodb_client(is_resource: bool = False):
    region_name = os.environ.get('AWS_REGION', 'us-east-1')
    if is_resource:
        return boto3.resource('dynamodb', region_name=region_name)
    else:
        return boto3.client('dynamodb', region_name=region_name)

def get_table_name():
    return os.environ.get('DYNAMODB_TABLE_NAME', 'DocumentsTable')
