import boto3

def embed_text(text: str) -> dict:
    client = boto3.client('sagemaker-runtime')
    response = client.invoke_endpoint(
        EndpointName='direct-embeddings-endpoint',
        ContentType='application/json',
        Body=json.dumps({'inputs': text})
    )
    result = json.loads(response['Body'].read().decode())
    return result['embedding']