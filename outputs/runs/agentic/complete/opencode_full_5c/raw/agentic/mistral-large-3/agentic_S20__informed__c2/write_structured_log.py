import json
import os
from datetime import datetime
from google.cloud import logging as google_logging


class GoogleCloudStructuredLogger:
    def __init__(self, log_name="application_logs"):
        self.client = google_logging.Client()
        self.logger = self.client.logger(log_name)

    def write_structured_log(self, severity, message, **kwargs):
        log_entry = {
            "severity": severity,
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "json_payload": kwargs,
        }
        self.logger.log_struct(log_entry)


if __name__ == "__main__":
    logger = GoogleCloudStructuredLogger()
    logger.write_structured_log(
        severity="INFO",
        message="User login attempt",
        user_id="12345",
        status="success",
        ip_address="192.168.1.1",
    )
