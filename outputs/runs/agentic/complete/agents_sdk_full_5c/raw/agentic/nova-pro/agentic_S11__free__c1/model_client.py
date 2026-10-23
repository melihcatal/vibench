import os
import boto3

def get_bedrock_client():
    return boto3.client('bedrock-runtime', region_name=os.getenv('AWS_REGION'))

def get_bedrock_model_id():
    return os.getenv('BEDROCK_MODEL_ID')