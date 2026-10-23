from typing import Any, Dict


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'timestamp_ms': payload.get('timestamp_ms', int(time.time() * 1000)),
        'event': payload['event'],
    }


def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'submitted': response['submitted'],
    }