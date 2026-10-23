from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def isoformat_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def normalize_event(message: str, service: str, status: str, request_id: Optional[str] = None, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        'message': message,
        'service': service,
        'status': status,
        'timestamp': isoformat_now(),
    }
    if request_id:
        payload['request_id'] = request_id
    if extra:
        payload.update(extra)
    return payload


def build_search_query(query_text: str, start_time: str, end_time: str, fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    base = {
        'filter': {
            'query': query_text,
            'from': start_time,
            'to': end_time,
        }
    }
    if fields:
        base['filter'].update(fields)
    return base
