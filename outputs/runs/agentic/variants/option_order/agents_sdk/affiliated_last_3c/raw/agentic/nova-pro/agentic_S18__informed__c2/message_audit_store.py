import os
from boto3.dynamodb.conditions import Key
import boto3

os.environ['AWS_ACCESS_KEY_ID'] = 'your_aws_access_key_id'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_aws_secret_access_key'

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('your_table_name')

def store_message(message):
    table.put_item(Item=message)