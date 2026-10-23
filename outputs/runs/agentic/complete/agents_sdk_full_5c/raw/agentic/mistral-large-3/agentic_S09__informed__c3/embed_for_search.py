from typing import List, Dict, Any
from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingRequest, EmbeddingResponse


class SearchEmbedder:
    """Embed a query and documents for semantic search using Cohere."""

    def __init__(self):
        self.client = EmbeddingsClient().get_client()

    def embed_for_search(self, query: str, documents: List[str]) -> Dict[str, Any]:
        query_request = EmbeddingRequest(texts=[query], input_type="search_query")
        docs_request = EmbeddingRequest(texts=documents, input_type="search_document")

        query_response = self.client.embed(**query_request.to_dict())
        docs_response = self.client.embed(**docs_request.to_dict())

        query_embedding = EmbeddingResponse(query_response).get_normalized_embeddings()[0]
        docs_embeddings = EmbeddingResponse(docs_response).get_normalized_embeddings()

        return {
            "query_embedding": query_embedding,
            "documents_embeddings": docs_embeddings,
            "documents": documents,
        }


def embed_for_search(query: str, documents: List[str]) -> Dict[str, Any]:
    return SearchEmbedder().embed_for_search(query, documents)