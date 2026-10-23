from typing import Dict, Any

def create_log_entry(message: str, severity: str = 'INFO', **kwargs) -> Dict[str, Any]:
    """Helper to create a structured log entry payload."""
    payload = {
        "message": message,
        "severity": severity,
    }
    payload.update(kwargs)
    return payload
