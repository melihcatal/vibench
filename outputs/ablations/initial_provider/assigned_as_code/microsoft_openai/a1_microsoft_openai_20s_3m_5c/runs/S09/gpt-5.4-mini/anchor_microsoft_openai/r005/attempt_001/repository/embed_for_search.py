from embed_batch import embed_batch
from embed_text import embed_text


def embed_for_search(payload, config=None):
    config = config or {}
    query = embed_text({'text': payload['query']}, config)['embedding']
    documents = embed_batch({'texts': payload['documents']}, config)['embeddings']
    return {'query_embedding': query, 'document_embeddings': documents}
