import boto3
import os

def get_dynamodb_client():
    return boto3.client('dynamodb', region_name=os.getenv('AWS_REGION'))