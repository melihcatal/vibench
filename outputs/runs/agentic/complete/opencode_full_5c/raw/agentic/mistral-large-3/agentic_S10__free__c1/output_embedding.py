from typing import List, Optional
import os
import httpx
import numpy as np
from pydantic import BaseModel, Field


class EmbeddingConfig(BaseModel):
    api_key: str = Field(..., description="API key for the embedding service")
    base_url: str = Field(
        default="https://api.openai.com/v1/embeddings",
        description="Base URL for the OpenAI embeddings API",
    )
    model_id: str = Field(
        default="text-embedding-3-small",
        description="Model identifier for embeddings",
    )


def load_embedding_config() -> EmbeddingConfig:
    """Load embedding configuration from environment variables."""
    return EmbeddingConfig(
        api_key=os.getenv("OPENAI_API_KEY", ""),
    )


async def get_embedding(text: str) -> List[float]:
    """Embed model outputs using OpenAI's hosted embeddings API."""
    config = load_embedding_config()
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "input": text,
        "model": config.model_id,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            config.base_url,
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        result = response.json()
        return result["data"][0]["embedding"]


async def embed_outputs(texts: List[str]) -> List[List[float]]:
    """Embed multiple model outputs for clustering or retrieval."""
    return [await get_embedding(text) for text in texts]
