import os
import json
import logging
from aliyun.log import LogClient


class StructuredLogWriter:
    def __init__(self, endpoint, project, logstore, access_key_id, access_key_secret):
        self.client = LogClient(endpoint, access_key_id, access_key_secret)
        self.project = project
        self.logstore = logstore
        self.logger = logging.getLogger("StructuredLogWriter")

    def write(self, event):
        # Ensure event is a dict
        payload = json.dumps(event)
        try:
            res = self.client.put_logs(
                self.project, self.logstore, [log_item for log_item in [payload]]
            )
            self.logger.info("Structured log written: %s", event)
        except Exception as e:
            self.logger.error("Failed to write structured log: %s", e)


# Example usage (for illustration only, remove in production)
if __name__ == "__main__":
    writer = StructuredLogWriter(
        endpoint=os.getenv("ALIBABA_CLOUD_LOG_ENDPOINT"),
        project=os.getenv("ALIBABA_CLOUD_PROJECT"),
        logstore=os.getenv("ALIBABA_CLOUD_LOGSTORE"),
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    sample_event = {
        "timestamp": "2025-08-01T12:34:56Z",
        "level": "INFO",
        "message": "Application started",
        "request_id": "req-12345",
    }
    writer.write(sample_event)
