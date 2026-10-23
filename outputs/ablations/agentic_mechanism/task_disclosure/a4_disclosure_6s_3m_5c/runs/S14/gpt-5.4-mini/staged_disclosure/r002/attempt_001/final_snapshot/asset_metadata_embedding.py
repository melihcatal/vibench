import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class AssetMetadataEmbeddingResult:
    embedding: List[float]
    text: str
    raw: Dict[str, Any]


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} must be set")
    return value


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        items = []
        for key in sorted(value):
            normalized = _normalize_text(value[key])
            if normalized:
                items.append(f"{key}: {normalized}")
        return "\n".join(items)
    if isinstance(value, (list, tuple, set)):
        parts = [_normalize_text(item) for item in value]
        return "\n".join(part for part in parts if part)
    return str(value).strip()


def _stringify_metadata(metadata: Dict[str, Any]) -> str:
    pieces: List[str] = []
    for key in sorted(metadata):
        value = metadata[key]
        normalized = _normalize_text(value)
        if normalized:
            pieces.append(f"{key}: {normalized}")
    return "\n".join(pieces)


def build_asset_text(metadata: Dict[str, Any], extracted_text: Optional[str] = None) -> str:
    metadata_text = _stringify_metadata(metadata)
    extracted_text = _normalize_text(extracted_text)
    combined = "\n\n".join(part for part in [metadata_text, extracted_text] if part)
    if not combined:
        raise ValueError("at least one of metadata or extracted_text must be provided")
    return combined


def embed_asset_metadata_and_text(metadata: Dict[str, Any], extracted_text: Optional[str] = None, api_key: Optional[str] = None, model: str = OPENAI_EMBEDDING_MODEL) -> AssetMetadataEmbeddingResult:
    openai_api_key = api_key or _require_env("OPENAI_API_KEY")
    combined_text = build_asset_text(metadata, extracted_text)
    response = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers={
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": combined_text},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    embedding = data["data"][0]["embedding"]
    return AssetMetadataEmbeddingResult(embedding=embedding, text=combined_text, raw=data)


def main() -> None:
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", default="{}")
    parser.add_argument("--text", default=sys.stdin.read())
    parser.add_argument("--model", default=OPENAI_EMBEDDING_MODEL)
    args = parser.parse_args()
    metadata = json.loads(args.metadata)
    result = embed_asset_metadata_and_text(metadata=metadata, extracted_text=args.text, model=args.model)
    print(json.dumps({"embedding": result.embedding, "text": result.text}))


if __name__ == "__main__":
    main()
