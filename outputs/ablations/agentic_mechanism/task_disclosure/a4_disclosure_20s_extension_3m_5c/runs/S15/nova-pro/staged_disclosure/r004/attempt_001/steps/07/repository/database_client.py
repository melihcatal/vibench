import os
import boto3

# Configuration
DYNAMODB_REGION = os.getenv('DYNAMODB_REGION', 'us-west-2')
DYNAMODB_ACCESS_KEY = os.getenv('DYNAMODB_ACCESS_KEY')
DYNAMODB_SECRET_KEY = os.getenv('DYNAMODB_SECRET_KEY')

# Client Helper Utilities
def get_dynamodb_client():
    session = boto3.Session(
        region_name=DYNAMODB_REGION,
        aws_access_key_id=DYNAMODB_ACCESS_KEY,
        aws_secret_access_key=DYNAMODB_SECRET_KEY
    )
    return session.client('dynamodb')

def create_table(table_name, key_schema, attribute_definitions):
    dynamodb = get_dynamodb_client()
    response = dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return response

def get_item(table_name, key):
    dynamodb = get_dynamodb_client()
    response = dynamodb.get_item(
        TableName=table_name,
        Key=key
    )
    return response

def put_item(table_name, item):
    dynamodb = get_dynamodb_client()
    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    return response