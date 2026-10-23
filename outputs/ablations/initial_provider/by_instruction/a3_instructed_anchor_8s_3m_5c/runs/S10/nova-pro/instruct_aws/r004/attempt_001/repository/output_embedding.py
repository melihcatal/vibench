import boto3
import json

def embed_output(text):
    client = boto3.client('sagemaker-runtime')
    endpoint_name = 'text-embedding-endpoint'
    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',
        Body=json.dumps({'inputText': text})
    )
    result = json.loads(response['Body'].read())
    return result['embedding']