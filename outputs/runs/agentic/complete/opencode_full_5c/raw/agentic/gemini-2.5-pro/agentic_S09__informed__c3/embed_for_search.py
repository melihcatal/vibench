from typing import List, Dict, Any
from embeddings_client import get_openai_client
from embeddings_models import EmbeddingRequest


def embed_for_search(query: str, documents: List[str]) -> Dict[str, Any]:
    """
    Embeds a query and a list of documents for semantic search using OpenAI.
    """
    client = get_openai_client()

    query_request = EmbeddingRequest(input=query)
    query_response = client.embeddings.create(
        input=query_request.input, model=query_request.model
    )
    query_embedding = query_response.data[0].embedding

    doc_request = EmbeddingRequest(input=documents)
    doc_response = client.embeddings.create(
        input=doc_request.input, model=doc_request.model
    )
    doc_embeddings = [item.embedding for item in doc_response.data]

    return {
        "query_embedding": query_embedding,
        "document_embeddings": doc_embeddings,
        "model": query_response.model,
    }
