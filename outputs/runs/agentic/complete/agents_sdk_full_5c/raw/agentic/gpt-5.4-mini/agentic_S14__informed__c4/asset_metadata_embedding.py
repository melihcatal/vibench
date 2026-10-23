from __future__ import annotations

from openai import OpenAI

from storage_models import EmbeddingResult

EMBEDDING_MODEL_ID = "text-embedding-3-small"


def asset_metadata_embedding(metadata: dict, extracted_text: str) -> EmbeddingResult:
    client = OpenAI()
    payload = f"metadata={metadata}\ntext={extracted_text}"
    response = client.embeddings.create(model=EMBEDDING_MODEL_ID, input=payload)
    vector = response.data[0].embedding
    return EmbeddingResult(text=payload, vector=vector, metadata=metadata)
