import os

from observability_client import write_json_log
from observability_models import LogWriteRequest, utc_now_iso


def main() -> dict:
    return write_json_log(
        LogWriteRequest(
            log_name=os.getenv("GOOGLE_CLOUD_LOG_NAME", "structured_app_log"),
            payload={
                "event": "structured_log_written",
                "service": "log-ingestion",
                "timestamp": utc_now_iso(),
                "severity": "INFO",
                "details": {"provider": "google_cloud_logging"},
            },
            severity="INFO",
        )
    )
