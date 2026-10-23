import os
from typing import Any, Dict, Iterable, List, Optional, Sequence, Union

from openai import OpenAI


def _normalize_output_text(platform_output: Any) -> str:
    if platform_output is None:
        return ""
    if isinstance(platform_output, str):
        return platform_output
    if isinstance(platform_output, dict):
        for key in ("output_text", "text", "content", "message", "response"):
            value = platform_output.get(key)
            if isinstance(value, str):
                return value
            if isinstance(value, list):
                parts: List[str] = []
                for item in value:
                    if isinstance(item, str):
                        parts.append(item)
                    elif isinstance(item, dict):
                        text = item.get("text") or item.get("content")
                        if isinstance(text, str):
                            parts.append(text)
                if parts:
                    return "\n".join(parts)
    return str(platform_output)


def _chunk_text(text: str, max_chars: int) -> List[str]:
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")
    if not text:
        return [""]
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars)]


def embed_platform_outputs(
    platform_outputs: Union[Any, Sequence[Any]],
    *,
    model: str = "text-embedding-3-small",
    max_chars_per_item: int = 8000,
    client: Optional[OpenAI] = None,
) -> List[Dict[str, Any]]:
    openai_client = client or OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    items = list(platform_outputs) if isinstance(platform_outputs, (list, tuple)) else [platform_outputs]
    texts: List[str] = []
    records: List[Dict[str, Any]] = []

    for index, item in enumerate(items):
        text = _normalize_output_text(item)
        for chunk_index, chunk in enumerate(_chunk_text(text, max_chars_per_item)):
            texts.append(chunk)
            records.append(
                {
                    "item_index": index,
                    "chunk_index": chunk_index,
                    "text": chunk,
                    "source": item,
                }
            )

    if not texts:
        return []

    response = openai_client.embeddings.create(model=model, input=texts)
    embeddings = [datum.embedding for datum in response.data]

    for record, embedding in zip(records, embeddings):
        record["embedding"] = embedding
        record["model"] = model
        record["provider"] = "openai"

    return records
