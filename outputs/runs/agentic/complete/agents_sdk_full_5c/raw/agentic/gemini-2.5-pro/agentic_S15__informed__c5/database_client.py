import os
import boto3

def get_db_resource():
    """
    Initializes and returns the Boto3 DynamoDB resource.
    Credentials and region are sourced from environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_REGION
    """
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    # The Boto3 client will automatically use credentials from environment variables
    # if they are present (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).
    dynamodb_resource = boto3.resource('dynamodb', region_name=aws_region)
    return dynamodb_resource

def get_table(table_name: str):
    """
    Returns a DynamoDB table object.

    :param table_name: The name of the DynamoDB table.
    :return: A Boto3 Table resource object.
    """
    dynamodb = get_db_resource()
    return dynamodb.Table(table_name)
