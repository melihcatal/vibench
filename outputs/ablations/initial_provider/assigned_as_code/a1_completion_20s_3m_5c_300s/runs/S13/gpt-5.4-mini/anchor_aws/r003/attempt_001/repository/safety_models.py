from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def normalize_text_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    return {"text": str(payload)}


def normalize_messages(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, dict) and "messages" in payload:
        messages = payload["messages"]
    else:
        messages = payload
    if not isinstance(messages, Iterable) or isinstance(messages, (str, bytes, dict)):
        return [{"text": str(messages)}]
    normalized = []
    for message in messages:
        if isinstance(message, dict):
            normalized.append(message)
        else:
            normalized.append({"text": str(message)})
    return normalized


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def normalize_thresholds(payload: Any) -> Dict[str, float]:
    if isinstance(payload, dict):
        thresholds = payload.get("thresholds", payload)
        if isinstance(thresholds, dict):
            return {str(k): float(v) for k, v in thresholds.items()}
    return {}


def build_segments(text: str) -> List[Dict[str, str]]:
    return [{"Text": text}]


def build_batch_items(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [{"text": normalize_text(message.get("text", message))} for message in messages]
