from __future__ import annotations

from typing import Dict, List

from openai import OpenAI

from storage_models import normalize_metadata

_EMBED_MODEL = "text-embedding-3-small"


def embed_asset_metadata(bucket: str, key: str, metadata: Dict[str, str], extracted_text: str) -> Dict[str, List[float]]:
    client = OpenAI()
    normalized = normalize_metadata(metadata)
    payload = [
        f"bucket: {bucket}",
        f"key: {key}",
        "metadata: " + ", ".join(f"{k}={v}" for k, v in sorted(normalized.items())),
        f"text: {extracted_text}",
    ]
    response = client.embeddings.create(model=_EMBED_MODEL, input="\n".join(payload))
    vector = response.data[0].embedding if response.data else []
    return {"bucket": bucket, "key": key, "model": _EMBED_MODEL, "embedding": vector}
