import boto3


def embed_platform_output(text):
    client = boto3.client('sagemaker-runtime')
    response = client.invoke_endpoint(
        EndpointName='text-embedding-endpoint',
        ContentType='text/plain',
        Body=text,
    )
    return response['Body'].read().decode('utf-8')