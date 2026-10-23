import os
import boto3

def embed_text(text):
    client = boto3.client('sagemaker-runtime', region_name=os.getenv('AWS_REGION', 'us-west-2'), aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = client.invoke_endpoint(EndpointName=os.getenv('SAGEMAKER_ENDPOINT_NAME'), ContentType='text/plain', Body=text)
    result = response['Body'].read()
    return result