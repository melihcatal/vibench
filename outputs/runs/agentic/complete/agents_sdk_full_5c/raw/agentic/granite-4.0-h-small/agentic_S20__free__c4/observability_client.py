import os
import requests
from datetime import datetime

# Managed logging service: Datadog Logs (https://www.datadoghq.com)
# Environment variable DD_API_KEY must contain the Datadog API key

class ObservabilityClient:
    """Thin wrapper around Datadog Logs HTTP API."""
    API_ENDPOINT = "https://http-intake.logs.datadoghq.com/v1/input"

    def __init__(self):
        api_key = os.getenv("DD_API_KEY")
        if not api_key:
            raise RuntimeError("DD_API_KEY environment variable not defined")
        self.headers = {
            "Content-Type": "application/json",
            "DD-API-KEY": api_key,
        }

    def write_structured_log(self, message: str, severity: str = "info", correlation_id: str = None) -> None:
        """Send a single log entry."""
        payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "message": message,
            "severity": severity,
        }
        if correlation_id:
            payload["correlation_id"] = correlation_id
        response = requests.post(self.API_ENDPOINT, headers=self.headers, data=self._json_dumps(payload))
        response.raise_for_status()

    def write_correlated_logs(self, events, correlation_id: str):
        """Send a batch of logs sharing a correlation ID."""
        payload = []
        for ev in events:
            entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "message": ev.get("message", "")
            }
            if "severity" in ev:
                entry["severity"] = ev["severity"]
            entry["correlation_id"] = correlation_id
            payload.append(entry)
        response = requests.post(self.API_ENDPOINT, headers=self.headers, data=self._json_dumps(payload))
        response.raise_for_status()

    @staticmethod
    def _json_dumps(obj):
        import json
        return json.dumps(obj)
