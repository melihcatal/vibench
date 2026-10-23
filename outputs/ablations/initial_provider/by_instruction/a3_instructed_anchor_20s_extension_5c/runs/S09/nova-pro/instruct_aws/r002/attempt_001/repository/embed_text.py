from embeddings_client import create_embeddings_client
from embeddings_models import EmbeddingRequest, normalize_payload

def embed_text(text):
    client = create_embeddings_client()
    request = EmbeddingRequest(text)
    payload = normalize_payload(request)
    response = client.invoke_endpoint(
        EndpointName='direct-embeddings',
        ContentType='application/json',
        Body=payload
    )
    return response['Body'].read().decode('utf-8')