import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        return " ".join(_coerce_text(v) for v in value if _coerce_text(v))
    if isinstance(value, dict):
        parts = []
        for key in sorted(value.keys()):
            text = _coerce_text(value[key])
            if text:
                parts.append(f"{key}: {text}")
        return "\n".join(parts)
    return str(value)


def _normalize_metadata(metadata: Optional[Dict[str, Any]]) -> str:
    if not metadata:
        return ""
    lines = []
    for key in sorted(metadata.keys()):
        value = metadata[key]
        text = _coerce_text(value)
        if text:
            lines.append(f"{key}: {text}")
    return "\n".join(lines)


def build_embedding_input(metadata: Optional[Dict[str, Any]] = None, extracted_text: Optional[str] = None) -> str:
    metadata_text = _normalize_metadata(metadata)
    extracted_text = _coerce_text(extracted_text)
    parts = []
    if metadata_text:
        parts.append("Metadata:\n" + metadata_text)
    if extracted_text:
        parts.append("Extracted text:\n" + extracted_text)
    return "\n\n".join(parts)


def embed_asset_metadata(
    metadata: Optional[Dict[str, Any]] = None,
    extracted_text: Optional[str] = None,
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
) -> List[float]:
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    content = build_embedding_input(metadata=metadata, extracted_text=extracted_text)
    if not content.strip():
        return []
    response = client.embeddings.create(model=model, input=content)
    return list(response.data[0].embedding)
