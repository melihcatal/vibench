import os
import boto3

dynamodb_resource = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME', 'Documents')

_table = dynamodb_resource.Table(TABLE_NAME)

def get_dynamodb_table():
    return _table