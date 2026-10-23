import boto3

def embed_for_search(query, documents):
    client = boto3.client('sagemaker-runtime')
    query_embedding = client.invoke_endpoint(
        EndpointName='amazon-sagemaker-endpoint',
        ContentType='text/plain',
        Body=query.encode('utf-8')
    )['Body'].read().decode('utf-8')
    document_embeddings = [client.invoke_endpoint(
        EndpointName='amazon-sagemaker-endpoint',
        ContentType='text/plain',
        Body=doc.encode('utf-8')
    )['Body'].read().decode('utf-8') for doc in documents]
    return query_embedding, document_embeddings