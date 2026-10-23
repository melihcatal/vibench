from embeddings_client import client
from embeddings_models import EmbeddingRequest, normalize_response

def embed_batch(texts: List[str]):
    requests = [EmbeddingRequest(input=text) for text in texts]
    response = client.embeddings.create(input=[req.input for req in requests], model='text-embedding-ada-002')
    return [normalize_response(r) for r in response['data']]