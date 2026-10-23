from __future__ import annotations

from openai import OpenAI

from storage_client import get_openai_api_key
from storage_models import EmbeddingResult


def embed_asset_metadata(metadata: dict, extracted_text: str) -> EmbeddingResult:
    client = OpenAI(api_key=get_openai_api_key())
    content = {
        "metadata": metadata,
        "extracted_text": extracted_text,
    }
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=str(content),
    )
    vector = response.data[0].embedding
    return EmbeddingResult(
        vector=vector,
        dimensions=len(vector),
        model="text-embedding-3-large",
        provider="openai",
    )
