from __future__ import annotations

from openai import OpenAI

from storage_client import get_openai_api_key
from storage_models import (
    AssetMetadataEmbeddingRequest,
    AssetMetadataEmbeddingResponse,
    build_embedding_input,
)


def embed_asset_metadata(
    request: AssetMetadataEmbeddingRequest,
) -> AssetMetadataEmbeddingResponse:
    model = "text-embedding-3-large"
    client = OpenAI(api_key=get_openai_api_key())
    input_text = build_embedding_input(
        bucket=request.bucket,
        object_key=request.object_key,
        metadata=request.metadata,
        extracted_text=request.extracted_text,
    )
    response = client.embeddings.create(model=model, input=input_text)
    vector = response.data[0].embedding
    return AssetMetadataEmbeddingResponse(
        provider="openai",
        model=model,
        vector=vector,
        dimensions=len(vector),
        input_text=input_text,
    )
