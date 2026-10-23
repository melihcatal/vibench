from __future__ import annotations

import os
from datetime import timedelta
from typing import Iterable

from google.cloud import monitoring_v3
from google.protobuf import duration_pb2
from google.protobuf import timestamp_pb2

from observability_models import MetricWindowRequest, ensure_utc


def get_google_cloud_project_id(project_id: str | None = None) -> str:
    value = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    if not value:
        raise ValueError(
            "A Google Cloud project id is required via argument, GOOGLE_CLOUD_PROJECT, or GCP_PROJECT"
        )
    return value


def get_metric_service_client() -> monitoring_v3.MetricServiceClient:
    return monitoring_v3.MetricServiceClient()


def project_name(project_id: str) -> str:
    return f"projects/{project_id}"


def make_time_interval(start_time, end_time) -> monitoring_v3.TimeInterval:
    start = timestamp_pb2.Timestamp()
    start.FromDatetime(ensure_utc(start_time))
    end = timestamp_pb2.Timestamp()
    end.FromDatetime(ensure_utc(end_time))
    return monitoring_v3.TimeInterval(start_time=start, end_time=end)


def make_aggregation(
    alignment_period_seconds: int, per_series_aligner: str
) -> monitoring_v3.Aggregation:
    period = duration_pb2.Duration()
    period.FromTimedelta(timedelta(seconds=alignment_period_seconds))
    aligner = getattr(monitoring_v3.Aggregation.Aligner, per_series_aligner)
    return monitoring_v3.Aggregation(
        alignment_period=period, per_series_aligner=aligner
    )


def list_time_series(request: MetricWindowRequest) -> Iterable:
    client = get_metric_service_client()
    pager = client.list_time_series(
        request={
            "name": project_name(request.project_id),
            "filter": request.build_filter(),
            "interval": make_time_interval(request.start_time, request.end_time),
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": make_aggregation(
                request.alignment_period_seconds, request.per_series_aligner
            ),
            "page_size": request.page_size,
        }
    )
    return pager
