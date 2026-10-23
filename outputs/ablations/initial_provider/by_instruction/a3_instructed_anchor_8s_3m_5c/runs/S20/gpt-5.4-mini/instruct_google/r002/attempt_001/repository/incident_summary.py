from typing import Dict, List

from google.cloud import logging as google_cloud_logging

from observability_client import query_entries, recent_time_window
from observability_models import LogQuery


def summarize_incident() -> Dict[str, object]:
    window = recent_time_window(minutes=120)
    query = LogQuery(severity="ERROR", **window)
    entries = query_entries(query, log_name="structured-log")
    return {
        "provider": "google-cloud-logging",
        "error_count": len(entries),
        "messages": [entry.get("payload", {}).get("message") for entry in entries[:10]],
    }


if __name__ == "__main__":
    summarize_incident()
