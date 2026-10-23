from __future__ import annotations

import os

from openai import OpenAI

from storage_models import AssetEmbeddingResult


def embed_asset_metadata(
    metadata: dict[str, str] | None, extracted_text: str
) -> AssetEmbeddingResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    metadata_lines = []
    if metadata:
        metadata_lines = [f"{key}: {value}" for key, value in sorted(metadata.items())]
    input_text = "\n".join(metadata_lines + ["", extracted_text]).strip()
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=input_text,
    )
    return AssetEmbeddingResult(
        provider="openai",
        model="text-embedding-3-large",
        input_text=input_text,
        embedding=response.data[0].embedding,
    )
