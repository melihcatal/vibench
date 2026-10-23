import json
import os
from datetime import datetime
from google.cloud import logging as google_logging


class GoogleCloudCorrelatedLogger:
    def __init__(self, log_name="correlated_logs"):
        self.client = google_logging.Client()
        self.logger = self.client.logger(log_name)

    def write_correlated_log(self, correlation_id, severity, message, **kwargs):
        log_entry = {
            "severity": severity,
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "correlation_id": correlation_id,
            "json_payload": kwargs,
        }
        self.logger.log_struct(log_entry)


if __name__ == "__main__":
    logger = GoogleCloudCorrelatedLogger()
    logger.write_correlated_log(
        correlation_id="req_67890",
        severity="INFO",
        message="Processing payment",
        user_id="12345",
        amount=99.99,
        currency="USD",
    )
