from typing import Dict, List


def normalize_log_event(event: Dict) -> Dict:
    return {
        "timestamp_ms": int(event.get("timestamp_ms", time.time() * 1000)),
        "event": event.get("event", {}),
    }


def parse_log_response(response: Dict) -> List[Dict]:
    return response.get("events", [])