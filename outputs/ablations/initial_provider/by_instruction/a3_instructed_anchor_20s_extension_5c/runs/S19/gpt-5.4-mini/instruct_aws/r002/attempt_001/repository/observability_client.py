import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import boto3


def load_config() -> Dict[str, Any]:
    return {
        "region_name": os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1",
        "namespace": os.getenv("AWS_METRICS_NAMESPACE", "Custom/Observability"),
    }


def cloudwatch_client():
    cfg = load_config()
    return boto3.client("cloudwatch", region_name=cfg["region_name"])


def to_utc(dt: Optional[datetime]) -> Optional[datetime]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def time_window_minutes(minutes: int):
    end_time = datetime.now(timezone.utc)
    start_time = end_time.fromtimestamp(end_time.timestamp() - minutes * 60, tz=timezone.utc)
    return start_time, end_time
