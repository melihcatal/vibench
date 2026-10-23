from embeddings_client import client
from embeddings_models import EmbeddingRequest, normalize_response

def embed_text(text: str):
    request = EmbeddingRequest(input=text)
    response = client.embeddings.create(input=request.input, model='text-embedding-ada-002')
    return normalize_response(response)