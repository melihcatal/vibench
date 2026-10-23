import boto3

sagemaker_runtime_client = boto3.client('sagemaker-runtime')

def embed_text(text, endpoint_name):
    response = sagemaker_runtime_client.invoke_endpoint(EndpointName=endpoint_name, ContentType='text/plain', Body=text)
    result = response['Body'].read()
    return result