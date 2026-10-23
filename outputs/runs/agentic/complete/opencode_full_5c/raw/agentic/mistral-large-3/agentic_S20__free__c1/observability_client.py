import os
from typing import Dict, List, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_logging_client():
    """
    Initializes and returns a Datadog logging client with retry logic.

    Returns:
        A configured requests Session for Datadog API interactions.
    """
    api_key = os.getenv("DATADOG_API_KEY")
    app_key = os.getenv("DATADOG_APP_KEY")

    if not api_key or not app_key:
        raise ValueError(
            "DATADOG_API_KEY and DATADOG_APP_KEY environment variables must be set"
        )

    session = requests.Session()
    session.headers.update(
        {
            "Content-Type": "application/json",
            "DD-API-KEY": api_key,
            "DD-APPLICATION-KEY": app_key,
        }
    )

    retry_strategy = Retry(
        total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)

    return session


def send_logs_to_datadog(session: requests.Session, logs: List[dict], endpoint: str):
    """
    Sends logs to Datadog's HTTP intake endpoint.

    Args:
        session: Configured requests Session
        logs: List of log events to send
        endpoint: Datadog logs intake endpoint
    """
    response = session.post(endpoint, json={"logs": logs})
    response.raise_for_status()


def query_datadog_logs(
    session: requests.Session, query: str, time_range: dict, limit: int, endpoint: str
) -> dict:
    """
    Queries Datadog logs API with the given parameters.

    Args:
        session: Configured requests Session
        query: Log query string
        time_range: Dictionary with 'from' and 'to' timestamps
        limit: Maximum number of logs to return
        endpoint: Datadog logs query endpoint

    Returns:
        Dictionary containing query results
    """
    payload = {
        "query": query,
        "time": time_range,
        "limit": limit,
        "sort": "-@timestamp",
    }

    response = session.post(endpoint, json=payload)
    response.raise_for_status()
    return response.json()


class LoggingClient:
    """
    Client wrapper for Datadog logging operations.
    """

    def __init__(self):
        self.session = get_logging_client()

    def send(self, logs: List[dict], endpoint: str, headers: Optional[Dict] = None):
        """Sends logs to Datadog."""
        if headers:
            original_headers = self.session.headers.copy()
            self.session.headers.update(headers)

        send_logs_to_datadog(self.session, logs, endpoint)

        if headers:
            self.session.headers = original_headers

    def query(self, query: str, time_range: dict, limit: int, endpoint: str) -> dict:
        """Queries Datadog logs."""
        return query_datadog_logs(self.session, query, time_range, limit, endpoint)
