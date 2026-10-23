import boto3

from security_client import get_bedrock_client

def get_bedrock_client():
    return boto3.client('bedrock-runtime')

def crypto_audit_embedding(text):
    bedrock_client = get_bedrock_client()
    model_id = 'amazon.titan-embed-text-v1'
    body = { 'inputText': text }
    response = bedrock_client.invoke_model(modelId=model_id, body=body)
    return response['embedding']