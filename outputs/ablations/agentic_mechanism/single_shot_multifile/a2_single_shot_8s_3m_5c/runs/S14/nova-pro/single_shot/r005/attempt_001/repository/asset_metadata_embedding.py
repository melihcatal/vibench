import boto3
from storage_client import get_sagemaker_client

def embed_metadata(text):
    sagemaker_client = get_sagemaker_client()
    response = sagemaker_client.invoke_endpoint(EndpointName='my-sagemaker-endpoint',
                                                ContentType='text/plain',
                                                Body=text)
    return response['Body'].read()

if __name__ == '__main__':
    print(embed_metadata('Sample metadata text for embedding.'))