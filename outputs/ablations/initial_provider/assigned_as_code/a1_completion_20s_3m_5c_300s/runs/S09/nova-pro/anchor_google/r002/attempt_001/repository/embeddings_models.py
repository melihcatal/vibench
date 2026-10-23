from.embeddings_client import get_embeddings_client

def normalize_embedding(embedding):
    return embedding / np.linalg.norm(embedding)

def parse_embedding_response(response):
    return response['data']