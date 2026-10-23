from google.cloud import logging as google_logging
from datetime import datetime, timedelta


class GoogleCloudLogFetcher:
    def __init__(self, log_name="application_logs"):
        self.client = google_logging.Client()
        self.logger = self.client.logger(log_name)

    def fetch_recent_logs(self, field_filters=None, hours=1):
        if field_filters is None:
            field_filters = {}

        filter_parts = [f'timestamp>="{datetime.utcnow() - timedelta(hours=hours)}"']
        for key, value in field_filters.items():
            filter_parts.append(f'jsonPayload.{key}="{value}"')

        filter_str = " ".join(filter_parts)
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
    fetcher = GoogleCloudLogFetcher()
    recent_logs = fetcher.fetch_recent_logs(field_filters={"user_id": "12345"}, hours=6)
    for log in recent_logs:
        print(log)
