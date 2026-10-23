import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        parts: List[str] = []
        for key in sorted(value.keys()):
            text = _to_text(value[key]).strip()
            if text:
                parts.append(f"{key}: {text}")
        return "\n".join(parts)
    if isinstance(value, (list, tuple, set)):
        parts = [_to_text(item).strip() for item in value]
        return "\n".join(part for part in parts if part)
    return str(value)


def build_embedding_text(metadata: Dict[str, Any], extracted_text: Optional[str]) -> str:
    metadata_text = _to_text(metadata).strip()
    extracted = (extracted_text or "").strip()
    pieces = []
    if metadata_text:
        pieces.append(f"Metadata:\n{metadata_text}")
    if extracted:
        pieces.append(f"Extracted text:\n{extracted}")
    return "\n\n".join(pieces)


def embed_asset_metadata(
    metadata: Dict[str, Any],
    extracted_text: Optional[str] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[float]:
    content = build_embedding_text(metadata, extracted_text)
    if not content:
        return []

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": content},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["data"][0]["embedding"]
