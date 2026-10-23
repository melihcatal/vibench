import boto3

def embed_batch(texts):
    client = boto3.client('sagemaker-runtime')
    embeddings = []
    for text in texts:
        response = client.invoke_endpoint(
            EndpointName='amazon-sagemaker-endpoint',
            ContentType='text/plain',
            Body=text.encode('utf-8')
        )
        result = response['Body'].read().decode('utf-8')
        embeddings.append(result)
    return embeddings