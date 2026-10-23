import boto3
import json

def embed_for_search(query: str, documents: list) -> list:
    client = boto3.client('sagemaker-runtime')
    query_embedding = client.invoke_endpoint(
        EndpointName='direct-embeddings-endpoint',
        ContentType='application/json',
        Body=json.dumps({'inputs': query})
    )
    query_embedding = json.loads(query_embedding['Body'].read().decode())['embedding']
    document_embeddings = embed_batch(documents)
    scores = [similarity_score(query_embedding, doc_emb) for doc_emb in document_embeddings]
    return scores