from typing import Dict, Any
from datetime import datetime, timedelta

def build_structured_payload(severity: str, message: str, **extra: Any) -> Dict[str, Any]:
    return {
        "severity": severity,
        "message": message,
        **extra
    }

def format_time(days_back: int = 1) -> str:
    return (datetime.utcnow() - timedelta(days=days_back)).strftime('%Y-%m-%dT%H:%M:%SZ')