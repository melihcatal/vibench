from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    return {'text': str(payload)}


def normalize_messages(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, dict) and 'messages' in payload:
        return payload['messages']
    if isinstance(payload, list):
        return payload
    return [{'text': str(payload)}]


def normalize_thresholds(config: Optional[Dict[str, Any]]) -> Dict[str, float]:
    config = config or {}
    return {k: float(v) for k, v in config.get('thresholds', {}).items()}
