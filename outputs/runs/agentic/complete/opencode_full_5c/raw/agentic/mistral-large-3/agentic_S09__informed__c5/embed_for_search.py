from typing import List, Dict, Tuple
import os
import google.generativeai as genai
from google.generativeai.types import ContentEmbedding

# Configure Gemini Embeddings
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class SearchEmbedder:
    def __init__(self, model: str = "models/embedding-001"):
        self.model = model

    def embed_for_search(
        self, query: str, documents: List[str]
    ) -> Tuple[List[float], List[List[float]]]:
        """
        Embeds a query and a list of documents for semantic search using Gemini Embeddings.
        Returns (query_embedding, document_embeddings).
        """
        query_embedding = genai.embed_content(
            model=self.model, content=query, task_type="retrieval_query"
        )["embedding"]

        document_embeddings = genai.embed_content(
            model=self.model, content=documents, task_type="retrieval_document"
        )["embedding"]

        return query_embedding, document_embeddings
