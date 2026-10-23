import os
from datetime import datetime, timedelta, timezone

from observability_client import query_logs
from observability_models import LogQueryRequest


def main() -> list:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=24)
    response = query_logs(
        LogQueryRequest(
            log_name=os.getenv("GOOGLE_CLOUD_LOG_NAME", "structured_app_log"),
            start_time=start_time.isoformat().replace("+00:00", "Z"),
            end_time=end_time.isoformat().replace("+00:00", "Z"),
            severity="ERROR",
            filters={"resource.type": "cloud_run_revision"},
        )
    )
    return response.entries
