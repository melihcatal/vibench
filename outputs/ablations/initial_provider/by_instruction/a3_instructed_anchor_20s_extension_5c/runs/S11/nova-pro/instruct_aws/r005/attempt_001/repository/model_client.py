import boto3
import json

def get_model_client():
    return boto3.client('bedrock-runtime', region_name='us-west-2')