import os
import boto3

# Configuration parameters
AWS_REGION = 'us-west-2'
BEDROCK_ENDPOINT_URL = 'https://bedrock.us-west-2.amazonaws.com'

# Helper utilities
def create_bedrock_client():
    return boto3.client('bedrock', region_name=AWS_REGION, endpoint_url=BEDROCK_ENDPOINT_URL)

def get_model_configuration(model_id):
    client = create_bedrock_client()
    response = client.get_model(modelId=model_id)
    return response

def invoke_model(model_id, payload):
    client = create_bedrock_client()
    response = client.invoke_model(modelId=model_id, body=payload)
    return response