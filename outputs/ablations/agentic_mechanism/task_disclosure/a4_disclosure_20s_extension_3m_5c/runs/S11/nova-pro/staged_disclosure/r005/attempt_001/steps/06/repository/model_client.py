import os
import boto3

BEDROCK_REGION = 'us-west-2'

def get_bedrock_client():
    bedrock_client = boto3.client('bedrock', region_name=BEDROCK_REGION)
    return bedrock_client

def list_models():
    client = get_bedrock_client()
    response = client.list_foundation_models()
    return response['modelSummaries']