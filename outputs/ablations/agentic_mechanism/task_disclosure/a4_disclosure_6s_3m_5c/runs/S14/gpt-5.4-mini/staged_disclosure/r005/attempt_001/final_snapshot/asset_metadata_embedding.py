import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        parts = []
        for key in sorted(value.keys()):
            text = _coerce_text(value[key]).strip()
            if text:
                parts.append(f"{key}: {text}")
        return "\n".join(parts)
    if isinstance(value, (list, tuple, set)):
        parts = [_coerce_text(item).strip() for item in value]
        return "\n".join(part for part in parts if part)
    return str(value)


def build_asset_search_text(metadata: Dict[str, Any], extracted_text: Optional[str] = None) -> str:
    metadata_text = _coerce_text(metadata).strip()
    extracted_text = (extracted_text or "").strip()
    combined = []
    if metadata_text:
        combined.append(metadata_text)
    if extracted_text:
        combined.append(extracted_text)
    return "\n\n".join(combined)


def embed_asset_metadata(metadata: Dict[str, Any], extracted_text: Optional[str] = None, model: str = "text-embedding-3-small") -> List[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    input_text = build_asset_search_text(metadata, extracted_text)
    response = client.embeddings.create(model=model, input=input_text)
    return response.data[0].embedding
