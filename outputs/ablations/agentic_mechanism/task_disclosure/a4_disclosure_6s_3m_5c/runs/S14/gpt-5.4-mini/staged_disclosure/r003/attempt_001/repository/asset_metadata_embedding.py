import os
from typing import Any, Dict, Iterable, List, Sequence

import requests


OPENAI_EMBEDDING_API_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _stringify_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        parts = []
        for key in sorted(value):
            rendered = _stringify_value(value[key])
            if rendered:
                parts.append(f"{key}: {rendered}")
        return " | ".join(parts)
    if isinstance(value, (list, tuple, set)):
        return " | ".join(part for part in (_stringify_value(item) for item in value) if part)
    return str(value)


def _normalize_text_chunks(text: Any) -> List[str]:
    if text is None:
        return []
    if isinstance(text, bytes):
        decoded = text.decode("utf-8", errors="replace").strip()
        return [decoded] if decoded else []
    if isinstance(text, str):
        stripped = text.strip()
        return [stripped] if stripped else []
    if isinstance(text, dict):
        for key in ("text", "content", "body", "extracted_text", "ocr_text"):
            if key in text:
                return _normalize_text_chunks(text[key])
        return []
    if isinstance(text, (list, tuple, set)):
        chunks: List[str] = []
        for item in text:
            chunks.extend(_normalize_text_chunks(item))
        return chunks
    rendered = str(text).strip()
    return [rendered] if rendered else []


def build_asset_embedding_input(asset: Any, extracted_text: Any = None, metadata_keys: Sequence[str] | None = None) -> str:
    metadata_text = ""
    if isinstance(asset, dict):
        keys: Iterable[str]
        if metadata_keys is None:
            keys = sorted(asset.keys())
        else:
            keys = metadata_keys
        rendered_pairs = []
        for key in keys:
            if key in asset:
                rendered = _stringify_value(asset[key])
                if rendered:
                    rendered_pairs.append(f"{key}: {rendered}")
        metadata_text = "\n".join(rendered_pairs)
    else:
        metadata_text = _stringify_value(asset)

    text_chunks = _normalize_text_chunks(extracted_text)
    sections = []
    if metadata_text:
        sections.append(f"METADATA\n{metadata_text}")
    if text_chunks:
        sections.append("EXTRACTED_TEXT\n" + "\n".join(text_chunks))
    return "\n\n".join(sections).strip()


def embed_asset_metadata(asset: Any, extracted_text: Any = None, metadata_keys: Sequence[str] | None = None) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    input_text = build_asset_embedding_input(asset, extracted_text=extracted_text, metadata_keys=metadata_keys)
    if not input_text:
        raise ValueError("No metadata or extracted text available to embed")

    response = requests.post(
        OPENAI_EMBEDDING_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_EMBEDDING_MODEL,
            "input": input_text,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    data = payload.get("data", [])
    if not data:
        raise RuntimeError("No embedding returned by OpenAI")
    embedding = data[0].get("embedding")
    if embedding is None:
        raise RuntimeError("Embedding payload missing vector")
    return {
        "embedding": embedding,
        "model": OPENAI_EMBEDDING_MODEL,
        "input": input_text,
        "raw_response": payload,
    }
