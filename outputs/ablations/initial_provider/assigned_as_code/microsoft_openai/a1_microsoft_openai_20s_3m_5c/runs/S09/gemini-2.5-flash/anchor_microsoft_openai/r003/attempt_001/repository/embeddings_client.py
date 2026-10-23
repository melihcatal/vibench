import os
from openai import OpenAI
from embeddings_models import EmbeddingRequest, EmbeddingResponse, SearchRequest, SearchResponse
from typing import Dict, Any, List

class EmbeddingsClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided or found in environment variables.")
        self.client = OpenAI(api_key=self.api_key)

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        response = self.client.embeddings.create(model=request.model, input=request.texts)
        return EmbeddingResponse(embeddings=[d.embedding for d in response.data])

    def embed_for_search(self, request: SearchRequest) -> SearchResponse:
        query_embedding_response = self.client.embeddings.create(model=request.model, input=request.query)
        document_embedding_response = self.client.embeddings.create(model=request.model, input=request.documents)
        return SearchResponse(
            query_embedding=query_embedding_response.data[0].embedding,
            document_embeddings=[d.embedding for d in document_embedding_response.data]
        )
