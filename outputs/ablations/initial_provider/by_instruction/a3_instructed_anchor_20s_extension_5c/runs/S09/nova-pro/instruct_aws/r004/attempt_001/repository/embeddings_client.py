import boto3
import json

def get_embeddings_client():
    return boto3.client('sagemaker-runtime')

def normalize_payload(text: str):
    return {'inputs': text}

def parse_response(response):
    return json.loads(response['Body'].read().decode())['embedding']