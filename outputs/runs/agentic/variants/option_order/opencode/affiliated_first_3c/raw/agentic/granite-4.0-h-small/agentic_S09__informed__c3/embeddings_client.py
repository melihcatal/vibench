import os
from ibm_watsonx_ai import WatsonX
from ibm_watsonx_ai.services import EmbEmbeddingsService

class EmbeddingsClient:
    """Local helper client providing configuration and helper utilities for the Direct Embeddings API.

    The client abstracts connection handling and provides convenience methods to generate
    single or batch embeddings, perform similarity scoring, and embed texts for search.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            api_key = os.getenv("WATSONX_API_KEY")
            project_id = os.getenv("WATSONX_PROJECT_ID")
            if not api_key or not project_id:
                raise RuntimeError("Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables")
            cls._instance = WatsonX(api_key=api_key)
        return cls._instance
    
    @property
    def embeddings_service(self) -> EmbEmbeddingsService:
        """Return an initialized EmbeddingsService ready for API calls."""
        return EmbEmbeddingsService(project_id=self._instance.project_id, api_key=self._instance.api_key)
    
    def embed_text(self, text: str) -> list[float]:
        """Generate a single embedding."""
        service = self.embeddings_service
nclient = EmbeddingsClient()
        response = service.create_embed(text=text)
        return response['embedding']
    
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        service = self.embeddings_service
        response = service.create_embed(text=texts)
        return [vec['embedding'] for vec in response]
    
    def similarity(self, vec1: list[float], vec2: list[float]) -> float:
        from .similarity_score import cosine_similarity
        return cosine_similarity(vec1, vec2)
    
    def search(self, query: str, corpus: list[str]) -> dict[int, float]:
        """Embed a query and a corpus, then compute similarity scores."""
        query_emb = self.embed_text(query)
        doc_embs = self.embed_batch(corpus)
        results = {}
        for i, vec in enumerate(doc_embs):
            results[i] = self.similarity(query_emb, vec)
        return results
