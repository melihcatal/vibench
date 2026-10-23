import os
import boto3

# Configure AWS credentials from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION', 'us-west-2')

# Create a DynamoDB client
dynamodb_client = boto3.client(
    'dynamodb',
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

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