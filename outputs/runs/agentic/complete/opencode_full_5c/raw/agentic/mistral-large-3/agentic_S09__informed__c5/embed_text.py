from typing import List, Optional
import os
import google.generativeai as genai
from google.generativeai.types import ContentEmbedding

# Configure Gemini Embeddings
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class TextEmbedder:
    def __init__(self, model: str = "models/embedding-001"):
        self.model = model

    def embed_text(self, text: str) -> List[float]:
        """
        Generates an embedding vector for a single text string using Gemini Embeddings.
        """
        result = genai.embed_content(
            model=self.model, content=text, task_type="retrieval_document"
        )
        return result["embedding"]
