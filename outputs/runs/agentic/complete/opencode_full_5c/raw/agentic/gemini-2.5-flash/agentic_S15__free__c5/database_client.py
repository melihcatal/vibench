import boto3
import os


def get_dynamodb_client():
    """
    Returns a configured AWS DynamoDB client.
    Uses environment variables for AWS credentials and region.
    """
    region = os.environ.get("AWS_REGION", "us-east-1")
    # For local development or specific endpoint, uncomment and configure:
    # endpoint_url = os.environ.get("DYNAMODB_ENDPOINT_URL")
    # if endpoint_url:
    #     return boto3.client("dynamodb", region_name=region, endpoint_url=endpoint_url)
    return boto3.client("dynamodb", region_name=region)


def get_s3_client():
    """
    Returns a configured AWS S3 client.
    Uses environment variables for AWS credentials and region.
    """
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("s3", region_name=region)
