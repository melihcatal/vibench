from __future__ import annotations

from openai import OpenAI

from storage_client import get_openai_api_key
from storage_models import EmbeddingResult, ObjectMetadataResult, build_embedding_input


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_asset_metadata(
    metadata: ObjectMetadataResult, extracted_text: str
) -> EmbeddingResult:
    client = OpenAI(api_key=get_openai_api_key())
    embedding_input = build_embedding_input(metadata, extracted_text)
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=embedding_input,
    )
    vector = response.data[0].embedding
    return EmbeddingResult(
        vector=vector,
        dimensions=len(vector),
        model=OPENAI_EMBEDDING_MODEL,
        provider="OpenAI",
    )
