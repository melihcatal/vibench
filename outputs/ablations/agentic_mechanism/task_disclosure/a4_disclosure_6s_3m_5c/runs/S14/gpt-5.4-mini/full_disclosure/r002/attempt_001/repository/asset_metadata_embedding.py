from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

import requests

from storage_models import EmbeddingResult, StoredObjectMetadata


OPENAI_API_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def _extract_text(payload: Dict[str, Any]) -> str:
    texts: List[str] = []
    for item in payload.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if text:
                    texts.append(text)
    if texts:
        return "\n".join(texts).strip()
    return str(payload.get("output_text", "")).strip()


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace").strip()
    return str(value).strip()


def _metadata_items(metadata: Mapping[str, Any]) -> List[str]:
    items: List[str] = []
    for key in sorted(metadata.keys(), key=str):
        value = metadata.get(key)
        if value is None:
            continue
        text = _normalize_text(value)
        if text:
            items.append(f"{key}: {text}")
    return items


def build_embedding_text(metadata: Optional[Mapping[str, Any]] = None, extracted_text: str = "") -> str:
    metadata = metadata or {}
    parts: List[str] = []
    metadata_lines = _metadata_items(metadata)
    if metadata_lines:
        parts.append("Metadata:\n" + "\n".join(metadata_lines))
    extracted_text = _normalize_text(extracted_text)
    if extracted_text:
        parts.append("Extracted text:\n" + extracted_text)
    return "\n\n".join(parts).strip()


def _parse_embedding_response(payload: Mapping[str, Any]) -> EmbeddingResult:
    data = payload.get("data") or []
    vector: Sequence[float] = ()
    if data:
        first = data[0] or {}
        vector_value = first.get("embedding") or []
        vector = tuple(float(v) for v in vector_value if v is not None)
    return EmbeddingResult(vector=tuple(vector), dimensions=len(vector) if vector else None, raw=dict(payload))


def embed_asset_metadata(
    metadata: Optional[Mapping[str, Any]] = None,
    extracted_text: str = "",
    *,
    model: str = OPENAI_EMBEDDING_MODEL,
    timeout: int = 60,
) -> EmbeddingResult:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    input_text = build_embedding_text(metadata=metadata, extracted_text=extracted_text)
    if not input_text:
        return EmbeddingResult(vector=(), dimensions=None, raw={"data": []})

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": input_text},
        timeout=timeout,
    )
    response.raise_for_status()
    return _parse_embedding_response(response.json())


def embed_stored_object(
    object_metadata: StoredObjectMetadata,
    extracted_text: str = "",
    *,
    model: str = OPENAI_EMBEDDING_MODEL,
    timeout: int = 60,
) -> Dict[str, Any]:
    embedding = embed_asset_metadata(
        metadata={
            "bucket": object_metadata.bucket,
            "key": object_metadata.key,
            "etag": object_metadata.etag,
            "size": object_metadata.size,
            "content_type": object_metadata.content_type,
            "content_encoding": object_metadata.content_encoding,
            "content_language": object_metadata.content_language,
            "cache_control": object_metadata.cache_control,
            "content_disposition": object_metadata.content_disposition,
            "last_modified": object_metadata.last_modified.isoformat() if object_metadata.last_modified else None,
            "storage_class": object_metadata.storage_class,
            "version_id": object_metadata.version_id,
            "checksum": object_metadata.checksum,
            **object_metadata.custom_metadata,
        },
        extracted_text=extracted_text,
        model=model,
        timeout=timeout,
    )
    return {
        "bucket": object_metadata.bucket,
        "key": object_metadata.key,
        "embedding": embedding.vector,
        "dimensions": embedding.dimensions,
        "model": model,
    }
