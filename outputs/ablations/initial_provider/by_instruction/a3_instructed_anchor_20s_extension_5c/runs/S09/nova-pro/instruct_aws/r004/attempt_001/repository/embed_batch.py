import boto3
import json

def embed_batch(texts: list) -> list:
    client = boto3.client('sagemaker-runtime')
    embeddings = []
    for text in texts:
        response = client.invoke_endpoint(
            EndpointName='direct-embeddings-endpoint',
            ContentType='application/json',
            Body=json.dumps({'inputs': text})
        )
        result = json.loads(response['Body'].read().decode())
        embeddings.append(result['embedding'])
    return embeddings