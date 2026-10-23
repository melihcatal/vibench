from embed_text import embed_text
from embed_batch import embed_batch

def embed_for_search(query: str, documents: list[str]) -> tuple[list[float], list[list[float]]]:
    # Embed the query using the single text embedding function
    query_embedding = embed_text(query)
    
    # Embed the documents using the batch embedding function
    document_embeddings = embed_batch(documents)
    
    return query_embedding, document_embeddings
