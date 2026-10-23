import json
import requests
from observability_client import get_log_service_url, get_auth_header


def write_structured_log(log_event):
    """Write a structured JSON log event to a managed logging service.

    The function sends a POST request with a JSON payload to the configured
    logging endpoint. It uses the provider-specific URL and authentication
    header (e.g., Datadog Logs HTTP API).
    """
    url = get_log_service_url()
    headers = {**get_auth_header(), "Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(log_event))
        response.raise_for_status()
        print(f"Log written successfully: {response.status_code}")
    except requests.RequestException as e:
        print(f"Failed to write log: {e}")


if __name__ == "__main__":
    example_event = {
        "timestamp": "2025-08-01T12:34:56Z",
        "level": "INFO",
        "service": "auth-service",
        "message": "User authenticated",
        "request_id": "req-12345",
    }
    write_structured_log(example_event)
