import os
import boto3
from botocore.exceptions import ClientError

def get_dynamodb_client() -> boto3.client:
    """Return a configured DynamoDB client using environment credentials.
    Requires AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY (or IAM role) and
    the endpoint URL if using DynamoDB local or a VPC endpoint.
    """
    region = os.getenv('AWS_REGION', 'us-east-1')
    endpoint = os.getenv('DYNAMODB_ENDPOINT')
    client = boto3.client(
        'dynamodb',
        region_name=region,
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        endpoint_url=endpoint
    )
    return client
