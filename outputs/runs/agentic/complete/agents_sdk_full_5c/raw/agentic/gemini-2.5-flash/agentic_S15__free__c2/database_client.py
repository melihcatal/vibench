import boto3
import os

def get_dynamodb_client():
    """
    Provides a configured boto3 DynamoDB client.
    Reads AWS region from environment variable AWS_REGION.
    """
    aws_region = os.getenv('AWS_REGION', 'us-east-1') # Default to us-east-1 if not set
    try:
        dynamodb = boto3.client('dynamodb', region_name=aws_region)
        print(f"DynamoDB client initialized for region: {aws_region}")
        return dynamodb
    except Exception as e:
        print(f"Error initializing DynamoDB client: {e}")
        raise

def get_dynamodb_resource():
    """
    Provides a configured boto3 DynamoDB resource.
    """
    aws_region = os.getenv('AWS_REGION', 'us-east-1')
    try:
        dynamodb = boto3.resource('dynamodb', region_name=aws_region)
        print(f"DynamoDB resource initialized for region: {aws_region}")
        return dynamodb
    except Exception as e:
        print(f"Error initializing DynamoDB resource: {e}")
        raise

if __name__ == '__main__':
    # Example usage
    # os.environ['AWS_REGION'] = 'eu-west-1'
    # client = get_dynamodb_client()
    # resource = get_dynamodb_resource()
    # print(client)
    # print(resource)
