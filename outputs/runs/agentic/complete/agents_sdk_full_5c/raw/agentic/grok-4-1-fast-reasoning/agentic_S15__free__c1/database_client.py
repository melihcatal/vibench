import os
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

TABLE_NAME = os.getenv('DYNAMODB_TABLE', 'Documents')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def get_table():
    return table
