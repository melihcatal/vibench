import os
from typing import List
from openai import OpenAI
from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    text: str
    model: str = "text-embedding-3-small"


class EmbeddingResponse(BaseModel):
    embedding: List[float]
    model: str


def embed_output(text: str, model: str = "text-embedding-3-small") -> EmbeddingResponse:
    """
    Embed model outputs for clustering or retrieval using OpenAI Embeddings.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        input=text,
        model=model
    )
    
    return EmbeddingResponse(
        embedding=response.data[0].embedding,
        model=response.model
    )