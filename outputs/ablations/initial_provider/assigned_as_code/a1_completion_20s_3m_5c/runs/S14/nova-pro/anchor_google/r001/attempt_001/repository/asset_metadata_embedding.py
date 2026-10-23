import boto3

def embed_metadata(metadata):
    client = boto3.client('sagemaker')
    response = client.invoke_endpoint(
        EndpointName='metadata-embedding-endpoint',
        ContentType='application/json',
        Body=json.dumps(metadata)
    )
    return response['Body'].read()