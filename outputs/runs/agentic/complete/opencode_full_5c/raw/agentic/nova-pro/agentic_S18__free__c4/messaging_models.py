from typing import Dict, Any


def normalize_message(message: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "body": message.get("body", ""),
        "event_type": message.get("event_type", "default"),
    }
