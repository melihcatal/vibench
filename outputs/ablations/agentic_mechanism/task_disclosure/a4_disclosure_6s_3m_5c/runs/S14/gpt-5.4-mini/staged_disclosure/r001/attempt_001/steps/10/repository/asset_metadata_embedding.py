import json
import os
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        parts: List[str] = []
        for key in sorted(value.keys()):
            item = _normalize_text(value[key])
            if item:
                parts.append(f"{key}: {item}")
        return "\n".join(parts)
    if isinstance(value, (list, tuple, set)):
        parts = [_normalize_text(item) for item in value]
        return "\n".join([part for part in parts if part])
    return str(value).strip()


def build_metadata_text(metadata: Dict[str, Any], extracted_text: Optional[str] = None) -> str:
    sections: List[str] = []
    metadata_text = _normalize_text(metadata)
    if metadata_text:
        sections.append(metadata_text)
    extracted = _normalize_text(extracted_text)
    if extracted:
        sections.append(f"extracted_text:\n{extracted}")
    return "\n\n".join(sections)


def chunk_text(text: str, max_chars: int = 6000) -> List[str]:
    cleaned = _normalize_text(text)
    if not cleaned:
        return []
    if len(cleaned) <= max_chars:
        return [cleaned]
    chunks: List[str] = []
    start = 0
    while start < len(cleaned):
        end = min(len(cleaned), start + max_chars)
        if end < len(cleaned):
            split_at = cleaned.rfind("\n", start, end)
            if split_at > start + max_chars // 2:
                end = split_at
        chunk = cleaned[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end
    return chunks


def embed_asset_metadata(
    metadata: Dict[str, Any],
    extracted_text: Optional[str] = None,
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    payload = build_metadata_text(metadata, extracted_text)
    chunks = chunk_text(payload)
    if not chunks:
        return {"model": model, "embedding": [], "chunks": [], "text": ""}
    response = client.embeddings.create(model=model, input=chunks)
    embeddings = [item.embedding for item in response.data]
    if len(embeddings) == 1:
        embedding = embeddings[0]
    else:
        vector_length = len(embeddings[0])
        embedding = [sum(values) / len(embeddings) for values in zip(*embeddings)] if vector_length else []
    return {
        "model": model,
        "embedding": embedding,
        "chunks": chunks,
        "text": payload,
    }


def embed_asset_metadata_from_json(
    json_blob: str,
    extracted_text: Optional[str] = None,
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    data = json.loads(json_blob)
    if not isinstance(data, dict):
        raise ValueError("JSON metadata must decode to an object")
    return embed_asset_metadata(data, extracted_text=extracted_text, model=model, api_key=api_key)
