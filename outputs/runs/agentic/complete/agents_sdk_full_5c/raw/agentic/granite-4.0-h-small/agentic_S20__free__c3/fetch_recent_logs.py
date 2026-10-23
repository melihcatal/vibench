import os
from datetime import datetime, timedelta
from typing import List, Dict
from observability_client import ObservabilityClient
from observability_models import NormalizedLogRecord, LogFilter, QueryResponse

def fetch_recent_logs(seconds: int = 300, keyword: str = None) -> List[NormalizedLogRecord]:
    """
    Retrieve recent log entries (default last 5 minutes). Optional keyword searches the message field.
    Placeholder implementation using the managed provider's query capabilities.
    """
    filter_payload: LogFilter = {
        "start_time": (datetime.utcnow() - timedelta(seconds=seconds)).isoformat(),
        "end_time": datetime.utcnow().isoformat()
    }
    if keyword:
        filter_payload["keyword"] = keyword
    # Placeholder; replace with real provider query, e.g., client.query(filter_payload)
    response: QueryResponse = {
        "total_hits": 2,
        "logs": [
            {
                "timestamp": (datetime.utcnow() - timedelta(minutes=1)).isoformat(),
                "level": "INFO",
                "service": "auth-service",
                "message": "User login successful for uid=abc123",
                "correlation_id": None
            },
            {
                "timestamp": datetime.utcnow().isoformat(),
                "level": "WARN",
                "service": "payment-service",
                "message": "Card declined due to insufficient funds",
                "correlation_id": "txn-789"
            }
        ]
    }
    return response["logs"]
