import boto3
from document_client import get_sagemaker_client

client = get_sagemaker_client()

def embed_text(text):
    response = client.invoke_endpoint(EndpointName='text-embedding-endpoint', Body=text, ContentType='text/plain')
    return response['Body'].read()