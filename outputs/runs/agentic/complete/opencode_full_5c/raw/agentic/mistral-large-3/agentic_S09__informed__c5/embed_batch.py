from typing import List
import os
import google.generativeai as genai
from google.generativeai.types import ContentEmbedding

# Configure Gemini Embeddings
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class BatchTextEmbedder:
    def __init__(self, model: str = "models/embedding-001"):
        self.model = model

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a batch of texts using Gemini Embeddings.
        """
        result = genai.embed_content(
            model=self.model, content=texts, task_type="retrieval_document"
        )
        return result["embedding"]
