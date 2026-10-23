from __future__ import annotations

import os
from typing import Mapping, Optional

from openai import OpenAI

from storage_models import AssetMetadataEmbeddingResult


def embed_asset_metadata(
    bucket: str,
    key: str,
    metadata: Optional[Mapping[str, object]] = None,
    extracted_text: str = "",
) -> AssetMetadataEmbeddingResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = "text-embedding-3-large"
    parts = [f"bucket={bucket}", f"key={key}"]
    if metadata:
        parts.extend(f"{name}={value}" for name, value in metadata.items())
    if extracted_text:
        parts.append(f"text={extracted_text}")
    payload = "\n".join(parts)
    response = client.embeddings.create(model=model, input=payload)
    vector = list(response.data[0].embedding)
    return AssetMetadataEmbeddingResult(
        vector=vector,
        dimensions=len(vector),
        provider="openai",
        model=model,
    )
