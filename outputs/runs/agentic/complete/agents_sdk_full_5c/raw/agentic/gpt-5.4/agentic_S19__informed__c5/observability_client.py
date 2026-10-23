from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

from google.cloud import monitoring_v3
from google.protobuf.duration_pb2 import Duration


@dataclass
class MonitoringConfig:
    project_id: str
    credentials_path: Optional[str] = None



def load_config(project_id: Optional[str] = None) -> MonitoringConfig:
    resolved_project = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    if not resolved_project:
        raise ValueError("GOOGLE_CLOUD_PROJECT or project_id is required")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    return MonitoringConfig(project_id=resolved_project, credentials_path=credentials_path)



def get_metric_client() -> monitoring_v3.MetricServiceClient:
    return monitoring_v3.MetricServiceClient()



def project_name(project_id: str) -> str:
    return f"projects/{project_id}"



def build_time_interval(minutes: int) -> monitoring_v3.TimeInterval:
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=minutes)
    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(now.timestamp())},
        start_time={"seconds": int(start.timestamp())},
    )
    return interval



def build_aggregation(alignment_period_seconds: int = 60, per_series_aligner: str = "ALIGN_MEAN") -> monitoring_v3.Aggregation:
    aligner = getattr(monitoring_v3.Aggregation.Aligner, per_series_aligner)
    return monitoring_v3.Aggregation(
        alignment_period=Duration(seconds=alignment_period_seconds),
        per_series_aligner=aligner,
    )



def build_filter(metric_type: str, resource_type: Optional[str] = None, resource_labels: Optional[dict] = None, metric_labels: Optional[dict] = None) -> str:
    clauses = [f'metric.type = "{metric_type}"']
    if resource_type:
        clauses.append(f'resource.type = "{resource_type}"')
    for key, value in (resource_labels or {}).items():
        clauses.append(f'resource.labels.{key} = "{value}"')
    for key, value in (metric_labels or {}).items():
        clauses.append(f'metric.labels.{key} = "{value}"')
    return " AND ".join(clauses)
