import os
from typing import List
from cohere import Client
from pydantic import BaseModel


class EmbeddingResult(BaseModel):
    embeddings: List[List[float]]
    model: str


def embed_output(text: str) -> EmbeddingResult:
    """
    Embeds platform outputs for evaluation or retrieval using Cohere Embed API.
    """
    api_key = os.getenv("COHERE_API_KEY")
    client = Client(api_key)

    response = client.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_document"
    )

    return EmbeddingResult(
        embeddings=response.embeddings,
        model=response.model
    )