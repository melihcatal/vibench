import os
from openai import OpenAI
from typing import List, Dict, Any
from embeddings_models import EmbeddingRequest, EmbeddingResponse, BatchEmbeddingResponse

class EmbeddingsClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found. Please provide it or set the environment variable.")
        self.client = OpenAI(api_key=self.api_key)

    def embed(self, texts: List[str], model: str = 'text-embedding-3-small') -> BatchEmbeddingResponse:
        # OpenAI API expects a single string or a list of strings for the 'input' parameter
        # If a single text is provided, wrap it in a list for consistency and then unwrap the result
        is_single_text = False
        if isinstance(texts, str):
            texts = [texts]
            is_single_text = True

        response = self.client.embeddings.create(model=model, input=texts)
        embeddings = [data.embedding for data in response.data]

        if is_single_text:
            return EmbeddingResponse(embedding=embeddings[0]) # Return a single embedding if single text was input
        return BatchEmbeddingResponse(embeddings=embeddings)
