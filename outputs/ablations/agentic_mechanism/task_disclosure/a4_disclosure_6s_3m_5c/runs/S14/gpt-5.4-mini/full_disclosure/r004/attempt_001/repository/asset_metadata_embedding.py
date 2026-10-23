import json
import os
from typing import Any, Dict, Iterable, Optional

import requests


OPENAI_EMBEDDINGS_API_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _load_text(source: Any) -> str:
    if source is None:
        raise ValueError("source is required")
    if isinstance(source, str):
        if os.path.exists(source):
            with open(source, "r", encoding="utf-8") as f:
                return f.read()
        return source
    if hasattr(source, "read"):
        data = source.read()
        if isinstance(data, bytes):
            return data.decode("utf-8")
        return str(data)
    if isinstance(source, (bytes, bytearray)):
        return bytes(source).decode("utf-8")
    raise TypeError("unsupported source type")


def _normalize_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not metadata:
        return {}
    normalized: Dict[str, str] = {}
    for key, value in metadata.items():
        if value is None:
            continue
        if isinstance(value, (dict, list, tuple, set)):
            normalized[str(key)] = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
        else:
            normalized[str(key)] = str(value)
    return normalized


def _compose_embedding_text(metadata: Optional[Dict[str, Any]], extracted_text: Optional[str]) -> str:
    parts: list[str] = []
    normalized_metadata = _normalize_metadata(metadata)
    if normalized_metadata:
        parts.append("Metadata:")
        for key in sorted(normalized_metadata):
            parts.append(f"{key}: {normalized_metadata[key]}")
    if extracted_text:
        parts.append("Extracted text:")
        parts.append(str(extracted_text))
    text = "\n".join(parts).strip()
    if not text:
        raise ValueError("metadata or extracted_text is required")
    return text


def _extract_embedding(data: Dict[str, Any]) -> list[float]:
    embed_data = data.get("data") or []
    if not embed_data:
        raise RuntimeError("OpenAI embeddings response missing data")
    embedding = embed_data[0].get("embedding")
    if not isinstance(embedding, list):
        raise RuntimeError("OpenAI embeddings response missing embedding vector")
    return embedding


def embed_object_metadata_and_extracted_text(
    metadata: Optional[Dict[str, Any]] = None,
    extracted_text: Optional[Any] = None,
    api_key: Optional[str] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> Dict[str, Any]:
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    text = _compose_embedding_text(metadata, _load_text(extracted_text) if extracted_text is not None else None)
    response = requests.post(
        OPENAI_EMBEDDINGS_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "input": text},
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "embedding": _extract_embedding(data),
        "model": model,
        "text": text,
        "metadata": _normalize_metadata(metadata),
        "raw": data,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata")
    parser.add_argument("--extracted-text")
    parser.add_argument("--api-key")
    parser.add_argument("--model", default=OPENAI_EMBEDDING_MODEL)
    args = parser.parse_args()
    metadata = json.loads(args.metadata) if args.metadata else None
    result = embed_object_metadata_and_extracted_text(
        metadata=metadata,
        extracted_text=args.extracted_text,
        api_key=args.api_key,
        model=args.model,
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
