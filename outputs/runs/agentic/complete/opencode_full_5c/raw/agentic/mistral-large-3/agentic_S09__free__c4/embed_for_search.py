from typing import List, Dict
from embeddings_client import EmbeddingsClient
from embeddings_models import EmbedRequest, normalize_embedding


def embed_for_search(query: str, documents: List[str]) -> Dict[str, List[float]]:
    client = EmbeddingsClient()
    texts = [query] + documents
    request = EmbedRequest(texts=texts, input_type="search_query")
    embeddings = client.embed(request.texts, request.model, request.input_type)

    query_embedding = normalize_embedding(embeddings[0])
    doc_embeddings = [normalize_embedding(embedding) for embedding in embeddings[1:]]

    return {"query_embedding": query_embedding, "document_embeddings": doc_embeddings}
