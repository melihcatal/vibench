import os
from typing import Optional
from openai import OpenAI
from model_models import EmbeddingRequest, EmbeddingResponse


def embed_output(request: EmbeddingRequest) -> EmbeddingResponse:
    """Embed model output using OpenAI embeddings."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")
    
    client = OpenAI(api_key=api_key)
    
    response = client.embeddings.create(
        input=request.text,
        model="text-embedding-3-small",
    )
    
    return EmbeddingResponse(
        embedding=response.data[0].embedding,
        model_id=response.model,
    )