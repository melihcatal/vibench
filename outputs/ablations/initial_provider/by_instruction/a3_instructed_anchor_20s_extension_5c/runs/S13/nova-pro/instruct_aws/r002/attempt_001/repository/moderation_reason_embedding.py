import boto3

sagemaker = boto3.client('sagemaker')

def embed_moderation_rationale(text):
    response = sagemaker.invoke_endpoint(EndpointName='moderation-rationale-embedding', Body=text, ContentType='text/plain')
    return response
