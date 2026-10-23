import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

from google.cloud import monitoring_v3


@dataclass(frozen=True)
class TimeWindow:
    start_time: datetime
    end_time: datetime


def project_name_from_env() -> str:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or os.environ.get("GOOGLE_PROJECT_ID")
    if not project_id:
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT")
    return f"projects/{project_id}"


def get_monitoring_client() -> monitoring_v3.MetricServiceClient:
    return monitoring_v3.MetricServiceClient()


def parse_time_window(start_time: Optional[str] = None, end_time: Optional[str] = None, minutes: int = 60) -> TimeWindow:
    end = datetime.now(timezone.utc) if end_time is None else datetime.fromisoformat(end_time.replace("Z", "+00:00"))
    start = (end - timedelta(minutes=minutes)) if start_time is None else datetime.fromisoformat(start_time.replace("Z", "+00:00"))
    return TimeWindow(start_time=start, end_time=end)
