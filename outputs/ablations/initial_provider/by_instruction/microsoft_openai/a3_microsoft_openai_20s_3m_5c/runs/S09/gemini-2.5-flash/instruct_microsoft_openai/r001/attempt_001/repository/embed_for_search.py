from typing import List, Dict, Any
from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingResponse

def embed_for_search(query: str, documents: List[str], model: str = "text-embedding-ada-002") -> Dict[str, EmbeddingResponse]:
    client = EmbeddingsClient()
    query_embedding_response = client.get_embeddings(texts=[query], model=model)
    document_embeddings_response = client.get_embeddings(texts=documents, model=model)

    return {
        "query_embedding": query_embedding_response,
        "document_embeddings": document_embeddings_response
    }
