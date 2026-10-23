from __future__ import annotations

import os
from datetime import datetime
from typing import Optional

from google.cloud import monitoring_v3


def get_project_name() -> str:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
    return f"projects/{project_id}"


def monitoring_client() -> monitoring_v3.MetricServiceClient:
    return monitoring_v3.MetricServiceClient()


def get_time_interval(start: datetime, end: datetime) -> monitoring_v3.TimeInterval:
    return monitoring_v3.TimeInterval(start_time=start, end_time=end)
