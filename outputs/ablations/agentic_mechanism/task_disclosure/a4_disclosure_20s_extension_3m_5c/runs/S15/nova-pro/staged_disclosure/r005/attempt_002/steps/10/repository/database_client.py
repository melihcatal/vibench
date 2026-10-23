import boto3

# Configuration for DynamoDB client
DYNAMODB_REGION = 'us-west-2'
DYNAMODB_ENDPOINT_URL = 'https://dynamodb.us-west-2.amazonaws.com'

# Initialize DynamoDB client
dynamodb_client = boto3.client(
    'dynamodb',
    region_name=DYNAMODB_REGION,
    endpoint_url=DYNAMODB_ENDPOINT_URL
)

# Helper utilities

def create_table(table_name, key_schema, attribute_definitions, provisioned_throughput):
    return dynamodb_client.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput=provisioned_throughput
    )

def get_item(table_name, key):
    return dynamodb_client.get_item(
        TableName=table_name,
        Key=key
    )

def put_item(table_name, item):
    return dynamodb_client.put_item(
        TableName=table_name,
        Item=item
    )

def delete_item(table_name, key):
    return dynamodb_client.delete_item(
        TableName=table_name,
        Key=key
    )