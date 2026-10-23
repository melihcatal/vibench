import os
from typing import List
from openai import OpenAI
from model_models import EmbeddingRequest, EmbeddingResponse


def embed_text(text: str, model: str = "text-embedding-3-small") -> EmbeddingResponse:
    """Embed model outputs for clustering or retrieval using OpenAI embeddings."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model=model, input=text, encoding_format="float"
        )

        embedding_data = response.data[0]

        return EmbeddingResponse(
            embedding=embedding_data.embedding,
            dimensions=len(embedding_data.embedding),
            model_used=model,
        )
    except Exception as e:
        raise Exception(f"Failed to create embedding: {str(e)}")
