from embeddings_client import create_embeddings_client
from embeddings_models import EmbeddingRequest, normalize_payload

def embed_for_search(query, documents):
    client = create_embeddings_client()
    query_request = EmbeddingRequest(query)
    query_payload = normalize_payload(query_request)
    query_response = client.invoke_endpoint(
        EndpointName='direct-embeddings',
        ContentType='application/json',
        Body=query_payload
    )
    query_embedding = query_response['Body'].read().decode('utf-8')
    document_requests = [EmbeddingRequest(doc) for doc in documents]
    document_payloads = [normalize_payload(request) for request in document_requests]
    document_responses = []
    for payload in document_payloads:
        response = client.invoke_endpoint(
            EndpointName='direct-embeddings',
            ContentType='application/json',
            Body=payload
        )
        document_responses.append(response['Body'].read().decode('utf-8'))
    return query_embedding, document_responses