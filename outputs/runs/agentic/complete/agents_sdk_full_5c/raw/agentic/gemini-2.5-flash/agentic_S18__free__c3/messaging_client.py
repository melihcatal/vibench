import boto3
import os

def get_aws_region() -> str:
    """Retrieves the AWS region from environment variables or defaults to 'us-east-1'."""
    return os.environ.get("AWS_REGION", "us-east-1")

def get_sns_client():
    """Returns an AWS SNS client.

    The client is configured using default AWS credential chain and region.
    """
    region = get_aws_region()
    return boto3.client('sns', region_name=region)

def get_sqs_client():
    """Returns an AWS SQS client.

    The client is configured using default AWS credential chain and region.
    """
    region = get_aws_region()
    return boto3.client('sqs', region_name=region)

def get_comprehend_client():
    """Returns an AWS Comprehend client.

    The client is configured using default AWS credential chain and region.
    """
    region = get_aws_region()
    return boto3.client('comprehend', region_name=region)

def get_translate_client():
    """Returns an AWS Translate client.

    The client is configured using default AWS credential chain and region.
    """
    region = get_aws_region()
    return boto3.client('translate', region_name=region)

def get_dynamodb_client():
    """Returns an AWS DynamoDB client.

    The client is configured using default AWS credential chain and region.
    """
    region = get_aws_region()
    return boto3.client('dynamodb', region_name=region)

def get_dynamodb_resource():
    """Returns an AWS DynamoDB resource (higher-level abstraction).

    The resource is configured using default AWS credential chain and region.
    """
    region = get_aws_region()
    return boto3.resource('dynamodb', region_name=region)
