from google.cloud import logging as google_logging
from datetime import datetime, timedelta


class GoogleCloudErrorLogQuery:
    def __init__(self, log_name="application_logs"):
        self.client = google_logging.Client()
        self.logger = self.client.logger(log_name)

    def query_error_logs(self, severity="ERROR", hours=1):
        filter_str = f'severity={severity} timestamp>="{datetime.utcnow() - timedelta(hours=hours)}"'
        entries = self.client.list_entries(filter_=filter_str, page_size=100)
        return [
            {
                "timestamp": entry.timestamp.isoformat() + "Z",
                "severity": entry.severity,
                "message": entry.payload.get("message", ""),
                "json_payload": entry.payload.get("json_payload", {}),
            }
            for entry in entries
        ]


if __name__ == "__main__":
    query = GoogleCloudErrorLogQuery()
    error_logs = query.query_error_logs(severity="ERROR", hours=24)
    for log in error_logs:
        print(log)
