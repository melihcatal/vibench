import os
import json
import logging
import requests
from observability_client import (
    get_datadog_api_key,
    get_datadog_app_key,
    get_correlation_id,
)

BASE_URL = "https://api.datadoghq.com/api/v2/logs-logs"

s = requests.Session()
s.headers.update(
    {
        "Content-Type": "application/json",
        "DD-API-KEY": get_datadog_api_key(),
        "DD-APPLICATION-KEY": get_datadog_app_key(),
    }
)


class CorrelatedLogWriter:
    def __init__(self, service="datadog"):
        self.service = service
        self.logger = logging.getLogger("CorrelatedLogWriter")

    def write(self, event, request_id=None):
        payload = {"timestamp": event.get("timestamp"), "message": event.get("message")}
        if request_id:
            payload["ddtags"] = f"correlation_id:{request_id}"
        try:
            response = s.post(BASE_URL, json=[payload])
            response.raise_for_status()
            self.logger.info("Logged correlated event: %s", payload)
        except Exception as e:
            self.logger.error("Error logging correlated event: %s", e)


if __name__ == "__main__":
    writer = CorrelatedLogWriter()
    event = {
        "timestamp": "2025-08-01T12:34:56Z",
        "message": "User login successful",
        "username": "alice",
    }
    # Pull correlation ID from environment or helper
    corr_id = get_correlation_id()
    writer.write(event, request_id=corr_id)
