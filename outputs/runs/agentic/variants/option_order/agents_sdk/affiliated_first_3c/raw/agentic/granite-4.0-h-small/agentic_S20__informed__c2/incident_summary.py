import json
from observability_models import SimpleLogMsg
from typing import List

# Provider: Datadog Logs API (used for ingestion in same-scenario)
from observability_client import ObservabilityClient, LogPayload

# Mock client using Datadog's ingest API (real implementation would instantiate a client)
class DatadogClient:
    def __init__(self):
        self.api_key = os.getenv('DD_API_KEY')
        self.app_key = os.getenv('DD_APP_KEY')
    def ingest(self, payload: LogPayload) -> None:
        import requests
        url = 'https://http-intake.logs.datadoghq.com/v1/input'
        headers = {
            'Content-Type': 'application/json',
            'DD-API-KEY': self.api_key,
            'DD-APPLICATION-KEY': self.app_key
        }
        r = requests.post(url, headers=headers, json=payload, timeout=5)
        r.raise_for_status()

def summarize_incident(logs: List[SimpleLogMsg]) -> dict:
    """Create a concise incident summary from a list of log payloads."""
    summary = {
        'incident_id': 'INCIDENT_2025_08_15',
        'timestamp_range': f'{min(l["timestamp"] for l in logs)} – {max(l["timestamp"] for l in logs)}',
        'error_count': sum(1 for l in logs if l["level"] == "ERROR"),
        'warning_count': sum(1 for l in logs if l["level"] == "WARNING"),
        'top_correlation_ids': [l["correlation_id"] for l in logs if l["correlation_id"]][:5],
        'unique_sources': sorted({l["source"] for l in logs if l["source"]})
    }
    return summary

if __name__ == '__main__':
    # Example retrieval using the same-scenario client (Datadog mock)
    client = DatadogClient()
    recent = [
        {'message': 'Connection error to DB', 'timestamp': '2025-08-15T12:01:10Z', 'level': 'ERROR', 'correlation_id': 'c1'},
        {'message': 'Timeout occurred', 'timestamp': '2025-08-15T12:03:45Z', 'level': 'ERROR', 'correlation_id': 'c2'},
        {'message': 'User logged in', 'timestamp': '2025-08-15T12:02:05Z', 'level': 'INFO', 'correlation_id': None}
    ]
    summary = summarize_incident(recent)
    print(json.dumps(summary, indent=2))
