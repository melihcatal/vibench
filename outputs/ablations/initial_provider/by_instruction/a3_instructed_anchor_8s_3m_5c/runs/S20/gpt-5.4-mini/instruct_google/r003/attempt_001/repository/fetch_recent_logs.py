import os
from datetime import datetime, timedelta, timezone

from observability_client import get_recent_logs


def main() -> list:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=1)
    return get_recent_logs(
        os.getenv("GOOGLE_CLOUD_LOG_NAME", "structured_app_log"),
        start_time.isoformat().replace("+00:00", "Z"),
        end_time.isoformat().replace("+00:00", "Z"),
        filters={"severity": "INFO"},
    )
