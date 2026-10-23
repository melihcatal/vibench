from typing import List, Dict, Any
import os
import google.generativeai as genai
from google.generativeai.types import ContentEmbedding

# Configure Gemini Embeddings
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class EmbeddingJobSummarizer:
    def __init__(self, model: str = "models/embedding-001"):
        self.model = model

    def summarize_job(
        self, texts: List[str], embeddings: List[List[float]]
    ) -> Dict[str, Any]:
        """
        Summarizes the results of an embedding job using Gemini Embeddings.
        """
        embedding_dim = len(embeddings[0]) if embeddings else 0
        avg_embedding = (
            [sum(dim) / len(embeddings) for dim in zip(*embeddings)]
            if embeddings
            else []
        )

        return {
            "total_texts": len(texts),
            "embedding_dimension": embedding_dim,
            "average_embedding": avg_embedding,
            "model_used": self.model,
        }
