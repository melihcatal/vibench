from __future__ import annotations

from openai import OpenAI

from storage_client import openai_api_key
from storage_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_asset_metadata(
    metadata: dict[str, str] | None, extracted_text: str | None = None
) -> EmbeddingResult:
    metadata = metadata or {}
    parts = [f"{key}: {value}" for key, value in sorted(metadata.items())]
    if extracted_text:
        parts.append(extracted_text)
    input_text = "\n".join(parts)
    client = OpenAI(api_key=openai_api_key())
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=input_text)
    vector = response.data[0].embedding
    return EmbeddingResult(
        input_text=input_text,
        embedding=vector,
        model=OPENAI_EMBEDDING_MODEL,
        dimensions=len(vector),
        provider="openai",
    )
