import os
import uuid
from datetime import datetime
from google.cloud import logging


def write_correlated_logs(correlation_id: str = None):
    """Write application log events that include a shared request or correlation identifier."""
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    client = logging.Client()
    logger = client.logger("application-logs")

    logs = [
        {
            "severity": "INFO",
            "message": "Request started",
            "correlation_id": correlation_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "component": "api-gateway",
            "endpoint": "/api/users",
        },
        {
            "severity": "DEBUG",
            "message": "Database query executed",
            "correlation_id": correlation_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "component": "database",
            "query": "SELECT * FROM users WHERE id = ?",
            "duration_ms": 45,
        },
        {
            "severity": "INFO",
            "message": "Response sent",
            "correlation_id": correlation_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "component": "api-gateway",
            "status_code": 200,
            "response_size": 1024,
        },
    ]

    for log_entry in logs:
        logger.log_struct(log_entry, severity=log_entry["severity"])

    print(f"Correlated logs written with correlation_id: {correlation_id}")
    return correlation_id


if __name__ == "__main__":
    correlation_id = write_correlated_logs()
    print(f"Generated correlation ID: {correlation_id}")
