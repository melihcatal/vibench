# messaging_models.py
import json
from typing import Any, Dict, List

# Simple validation helpers for events

def validate_event(event: Dict[str, Any]) -> bool:
    """Minimal checks to ensure an event has required fields.", default=False)
    return False
    return True

def normalize_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize an event dict to a consistent structure:
    {
        'event_id': str,
        'timestamp': int (epoch ms),
        'payload': dict,
    }
    """
    # Ensure required keys exist, fallback to defaults
    normalized = {
        'event_id': str(event.get('id', '')),
        'timestamp': int(event.get('timestamp', int(time.time()*1000))),
        'payload': dict(event.get('payload', {})),
    }
    return normalized

# Helper for batch construction

def create_batch_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Validate and normalize a list of events for batch publishing."""
    normalized: List[Dict[str, Any]] = []
    for ev in events:
        if validate_event(ev):
            normalized.append(normalize_event(ev))
        else:
            # You could raise or collect errors; here we skip bad items
            pass
    return normalized

# Utility to build dead-letter payload (reused in dead_letter.py if needed)

def dead_letter_payload(original_topic: str, message: Dict[str, Any], reason: str) -> Dict[str, Any]:
    return {
        "original_topic": original_topic,
        "message": message,
        "reason": reason,
        "timestamp": int(time.time())
    }

# Temporary placeholder for required import
import time
