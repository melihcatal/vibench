from embed_text import embed_text
from embed_batch import embed_batch


def embed_for_search(payload, config=None):
    query = embed_text({"text": payload["query"]}, config=config)["embedding"]
    documents = embed_batch({"texts": payload["documents"]}, config=config)["embeddings"]
    return {"query_embedding": query, "document_embeddings": documents}
