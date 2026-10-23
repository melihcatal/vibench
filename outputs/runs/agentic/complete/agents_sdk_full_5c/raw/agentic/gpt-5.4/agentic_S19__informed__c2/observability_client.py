from __future__ import annotations

import os
from datetime import timedelta
from typing import Optional

from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.types import Aggregation, TimeInterval

from observability_models import MetricWindowRequest, utc_now


ALIGNER_MAP = {
    "mean": Aggregation.Aligner.ALIGN_MEAN,
    "max": Aggregation.Aligner.ALIGN_MAX,
    "min": Aggregation.Aligner.ALIGN_MIN,
    "sum": Aggregation.Aligner.ALIGN_SUM,
    "rate": Aggregation.Aligner.ALIGN_RATE,
    "delta": Aggregation.Aligner.ALIGN_DELTA,
}

REDUCER_MAP = {
    "mean": Aggregation.Reducer.REDUCE_MEAN,
    "max": Aggregation.Reducer.REDUCE_MAX,
    "min": Aggregation.Reducer.REDUCE_MIN,
    "sum": Aggregation.Reducer.REDUCE_SUM,
}


class GoogleCloudObservabilityClient:
    def __init__(self, credentials_path: Optional[str] = None) -> None:
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.client = monitoring_v3.MetricServiceClient()

    def project_name(self, project_id: str) -> str:
        return f"projects/{project_id}"

    def build_interval(self, minutes: int) -> TimeInterval:
        end = utc_now()
        start = end - timedelta(minutes=minutes)
        return TimeInterval(end_time=end, start_time=start)

    def build_filter(self, metric_type: str, extra_filter: Optional[str] = None) -> str:
        base = f'metric.type = "{metric_type}"'
        if extra_filter:
            return f"{base} AND {extra_filter}"
        return base

    def build_aggregation(self, request: MetricWindowRequest) -> Aggregation:
        aggregation = Aggregation(alignment_period={"seconds": request.interval_seconds})
        if request.aggregation_aligner:
            aggregation.per_series_aligner = ALIGNER_MAP[request.aggregation_aligner.lower()]
        if request.aggregation_reducer:
            aggregation.cross_series_reducer = REDUCER_MAP[request.aggregation_reducer.lower()]
        if request.group_by_fields:
            aggregation.group_by_fields.extend(request.group_by_fields)
        return aggregation

    def list_time_series(self, request: MetricWindowRequest, view: monitoring_v3.ListTimeSeriesRequest.TimeSeriesView = monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL):
        return self.client.list_time_series(
            request={
                "name": self.project_name(request.project_id),
                "filter": self.build_filter(request.metric_type, request.filter_expression),
                "interval": self.build_interval(request.minutes),
                "view": view,
                "aggregation": self.build_aggregation(request),
            }
        )
