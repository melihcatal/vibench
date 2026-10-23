import os
import boto3

def get_dynamodb_table(table_name: str = None):
    if table_name is None:
        table_name = os.getenv('DYNAMODB_TABLE_NAME', 'Documents')
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(table_name)
