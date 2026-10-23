from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def normalize_bytes(data):
    if data is None:
        return b""
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode("utf-8")
    return bytes(data)


def normalize_object_name(payload: Dict[str, Any]) -> str:
    return payload["object_name"]


def normalize_prefix(payload: Dict[str, Any]) -> str:
    return payload.get("prefix", "")


def normalize_language(payload: Dict[str, Any], default: str = "en") -> str:
    return payload.get("target_language", payload.get("language", default))


def normalize_labels(payload: Dict[str, Any]) -> List[str]:
    labels = payload.get("labels", [])
    if isinstance(labels, str):
        return [labels]
    return list(labels)


def normalize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(metadata or {})
    for key in ("size", "updated", "created"):
        if key in normalized and normalized[key] is not None:
            normalized[key] = str(normalized[key])
    return normalized


def build_text_for_embedding(metadata: Dict[str, Any], extracted_text: str) -> str:
    parts = []
    for key in ("object_name", "bucket", "content_type", "size"):
        value = metadata.get(key)
        if value:
            parts.append(f"{key}: {value}")
    if extracted_text:
        parts.append(extracted_text)
    return "\n".join(parts)
