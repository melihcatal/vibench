import boto3

def embed_text(text):
    sagemaker_client = boto3.client('sagemaker-runtime')
    response = sagemaker_client.invoke_endpoint(EndpointName='text-embedding-endpoint', ContentType='text/plain', Body=text)
    return response