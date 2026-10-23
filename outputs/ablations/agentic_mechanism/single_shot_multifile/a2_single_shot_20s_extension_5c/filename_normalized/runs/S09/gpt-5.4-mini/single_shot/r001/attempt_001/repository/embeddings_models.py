from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def _extract_data(response: Any) -> list[Any]:
    if response is None:
        return []
    data = getattr(response, "data", None)
    if data is None and isinstance(response, dict):
        data = response.get("data", [])
    return list(data or [])


def normalize_single_embedding(response: Any) -> list[float]:
    data = _extract_data(response)
    if not data:
        return []
    first = data[0]
    embedding = getattr(first, "embedding", None)
    if embedding is None and isinstance(first, dict):
        embedding = first.get("embedding", [])
    return [float(x) for x in (embedding or [])]


def normalize_embedding_list(response: Any) -> list[list[float]]:
    result: list[list[float]] = []
    for item in _extract_data(response):
        embedding = getattr(item, "embedding", None)
        if embedding is None and isinstance(item, dict):
            embedding = item.get("embedding", [])
        result.append([float(x) for x in (embedding or [])])
    return result


def coerce_texts(texts: Iterable[str]) -> list[str]:
    return [str(text) for text in texts]
