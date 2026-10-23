import boto3

def embed_text(text):
    client = boto3.client('sagemaker-runtime')
    response = client.invoke_endpoint(EndpointName='text-embedding-model', Body=text, ContentType='text/plain')
    return response['Body'].read()