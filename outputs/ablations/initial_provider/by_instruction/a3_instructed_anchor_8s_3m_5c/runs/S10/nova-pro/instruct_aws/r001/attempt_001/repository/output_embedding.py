import boto3
import json

def embed_output(text):
    client = boto3.client('sagemaker-runtime', region_name='us-east-1')
    response = client.invoke_endpoint(
        EndpointName='amazon-sagemaker-endpoint',
        ContentType='text/plain',
        Body=text
    )
    result = json.loads(response['Body'].read())
    return result['embedding']