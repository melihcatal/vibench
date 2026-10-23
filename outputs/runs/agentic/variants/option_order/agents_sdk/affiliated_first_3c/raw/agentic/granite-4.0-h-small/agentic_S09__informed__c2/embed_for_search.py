import os
from embeddings_client import get_embedder
from embeddings_models import RequestData, normalize_response

class EmbedForSearch:
    def __init__(self, api_key: str | None = None, project_id: str | None = None):
        self.client = get_embedder()

    def embed_for_search(self, query: str, documents: list[str]) -> tuple[list[float], list[list[float]]]:
        """Embed a query and a list of documents for semantic search."""
        request = RequestData(query=query, texts=documents)
        response = self.client.embed(request=request)
        normalized = normalize_response(response)
        return normalized['query_embedding'], normalized['document_embeddings']
