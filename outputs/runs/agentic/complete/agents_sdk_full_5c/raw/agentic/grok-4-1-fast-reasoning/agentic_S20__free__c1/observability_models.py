import json
from typing import Dict, Any, List
from datetime import datetime

def normalize_structured_log(message: str, level: str = "INFO", **kwargs: Any) -> Dict[str, Any]:
    """Normalize to Datadog structured log format."""
    log: Dict[str, Any] = {
        "message": message,
        "level": level,
        "service": "python-app",
        "type": "structured",
        **kwargs
    }
    if "timestamp" not in log:
        log["timestamp"] = datetime.utcnow().isoformat()
    return log

def build_query_body(query: str, from_time: datetime, to_time: datetime, limit: int = 100) -> Dict[str, Any]:
    """Build dict body for Datadog logs query API."""
    return {
        "query": query,
        "time": {
            "from": from_time.isoformat(),
            "to": to_time.isoformat()
        },
        "page": {
            "limit": limit
        }
    }

def parse_log_response(response_data: List[Any]) -> List[Dict[str, Any]]:
    """Parse Datadog LogsListResponse.data to simple log dicts."""
    logs = []
    for log in response_data or []:
        attrs = log.attributes
        log_dict = {
            "message": getattr(attrs, 'message', ''),
            "level": getattr(attrs, 'level', 'unknown'),
            "service": getattr(attrs, 'service', 'unknown'),
            "timestamp": getattr(attrs, 'timestamp', None),
        }
        logs.append(log_dict)
    return logs
