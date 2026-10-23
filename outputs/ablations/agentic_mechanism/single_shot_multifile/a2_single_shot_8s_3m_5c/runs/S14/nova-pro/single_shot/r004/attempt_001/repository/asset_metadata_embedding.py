import boto3
from storage_client import get_sagemaker_runtime_client

def embed_metadata(text):
    sagemaker_runtime_client = get_sagemaker_runtime_client()
    response = sagemaker_runtime_client.invoke_endpoint(
        EndpointName='my-sagemaker-endpoint',
        ContentType='text/plain',
        Body=text)
    result = response['Body'].read()
    return result

if __name__ == '__main__':
    print(embed_metadata('Sample text for embedding.'))