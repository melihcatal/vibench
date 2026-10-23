import boto3


def embed_script(script):
    client = boto3.client('sagemaker-runtime')
    response = client.invoke_endpoint(EndpointName='text-embedding-endpoint', ContentType='text/plain', Body=script)
    result = response['Body'].read()
    return result