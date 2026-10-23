from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Tuple
import os

@dataclass(frozen=True)
class MetricsConfig:
    project_id: Optional[str]
    timeout_seconds: int
    credentials_token: Optional[str]


def get_metrics_config() -> MetricsConfig:
    return MetricsConfig(project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"), timeout_seconds=int(os.getenv("OBSERVABILITY_TIMEOUT_SECONDS", "30")), credentials_token=os.getenv("GOOGLE_OAUTH_ACCESS_TOKEN") or os.getenv("GCP_ACCESS_TOKEN"))


def build_headers(cfg: MetricsConfig) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if cfg.credentials_token:
        headers["Authorization"] = f"Bearer {cfg.credentials_token}"
    return headers


def normalize_time_window(start_time: Optional[datetime], end_time: Optional[datetime], window_minutes: int) -> Tuple[datetime, datetime]:
    end_dt = end_time or datetime.now(timezone.utc)
    start_dt = start_time or (end_dt - timedelta(minutes=window_minutes))
    if start_dt.tzinfo is None:
        start_dt = start_dt.replace(tzinfo=timezone.utc)
    if end_dt.tzinfo is None:
        end_dt = end_dt.replace(tzinfo=timezone.utc)
    return start_dt, end_dt
