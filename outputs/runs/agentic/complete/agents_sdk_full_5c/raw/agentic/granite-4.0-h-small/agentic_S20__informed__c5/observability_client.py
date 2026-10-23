import os
from typing import Any, Dict

def get_google_logging_client() -> Any:
    """Creates and returns an authenticated Google Cloud Logging client.

    The client uses the environment variable GOOGLE_APPLICATION_CREDENTIALS
    for authentication. This function can be imported by other modules to
    avoid duplicating auth code.
    """
    try:
        from google.cloud import logging_v2
        client = logging_v2.Client()
        return client
    except ImportError as exc:
        raise RuntimeError('Google Cloud Logging library not installed') from exc

class LogWriter:
    """Helper class that abstracts log write operations to Google Cloud Logging."""
    def __init__(self):
        self.client = get_google_logging_client()
    def write_structured(self, resource: str, severity: str, message: Dict[str, Any]) -> Any:
        entry = {
            'severity': severity,
            'jsonPayload': message,
            'resource': {'type': resource}
        }
        return self.client.logger('your-log-name').log_struct(entry)
    def write_correlated(self, resource: str, correlation_id: str, logs: list) -> Any:
        entries = []
        for log in logs:
            entries.append({
                'severity': log.get('severity', 'INFO'),
                'jsonPayload': log,
                'resource': {'type': resource},
                'labels': {'correlation_id': correlation_id}
            })
        return self.client.logger('your-log-name').log_entries(entries)
