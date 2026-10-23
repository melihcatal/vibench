from embeddings_client import create_embeddings_client
from embeddings_models import EmbeddingRequest, normalize_payload

def embed_batch(texts):
    client = create_embeddings_client()
    requests = [EmbeddingRequest(text) for text in texts]
    payloads = [normalize_payload(request) for request in requests]
    responses = []
    for payload in payloads:
        response = client.invoke_endpoint(
            EndpointName='direct-embeddings',
            ContentType='application/json',
            Body=payload
        )
        responses.append(response['Body'].read().decode('utf-8'))
    return responses