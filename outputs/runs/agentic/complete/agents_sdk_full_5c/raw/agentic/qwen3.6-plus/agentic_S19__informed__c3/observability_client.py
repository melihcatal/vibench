"""Local configuration and client helper utilities for Managed Metrics Monitoring.

Wraps the Google Cloud Monitoring client (google-cloud-monitoring) with
convenience methods for authentication, project resolution, request building,
and response normalization.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.services.metric_service import MetricServiceClient

from observability_models import (
    AggregationKind,
    AggregationResult,
    AlignmentPeriod,
    DimensionFilter,
    MetricComparisonResult,
    MetricDataPoint,
    MetricQueryRequest,
    MetricSeries,
    build_aggregation_dict,
    normalize_gcm_series,
)


def get_gcm_credentials_path() -> Optional[str]:
    """Return GOOGLE_APPLICATION_CREDENTIALS path if configured."""
    return os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")


def build_metric_client(
    credentials_path: Optional[str] = None,
) -> MetricServiceClient:
    """Build a Google Cloud Monitoring MetricServiceClient.

    Uses GOOGLE_APPLICATION_CREDENTIALS environment variable when credentials_path
    is not explicitly provided.
    """
    if credentials_path:
        return MetricServiceClient.from_service_account_json(credentials_path)
    return MetricServiceClient()


def project_name(project_id: Optional[str] = None) -> str:
    """Resolve Google Cloud project name string.

    Falls back to GCP_PROJECT or GOOGLE_CLOUD_PROJECT environment variables.
    """
    if project_id:
        return f"projects/{project_id}"
    pid = os.environ.get("GCP_PROJECT") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if pid:
        return f"projects/{pid}"
    raise ValueError(
        "project_id must be provided or set GCP_PROJECT / GOOGLE_CLOUD_PROJECT environment variable"
    )


def default_time_window(
    minutes: int = 60,
    end_time: Optional[datetime] = None,
) -> Tuple[datetime, datetime]:
    """Return (start_time, end_time) for a default lookback window."""
    end = end_time or datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    return start, end


class ObservabilityClient:
    """High-level client for Managed Metrics Monitoring via Google Cloud Monitoring."""

    def __init__(
        self,
        client: Optional[MetricServiceClient] = None,
        project_id: Optional[str] = None,
    ) -> None:
        self._client = client or build_metric_client()
        self._project_id = project_id

    @property
    def parent(self) -> str:
        return project_name(self._project_id)

    def query_metric_window(
        self,
        metric_type: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        filter_expression: Optional[str] = None,
        minutes: int = 60,
    ) -> List[MetricSeries]:
        """Query recent datapoints for a named metric over a time window.

        Calls Google Cloud Monitoring list_time_series with VIEW_FULL.
        """
        start, end = default_time_window(minutes) if not (start_time and end_time) else (start_time, end_time)

        request_filter = f'metric.type = "{metric_type}"'
        if filter_expression:
            request_filter = f'{request_filter} AND {filter_expression}'

        interval = monitoring_v3.TimeInterval(
            start_time={"seconds": int(start.timestamp()), "nanos": start.microsecond * 1000},
            end_time={"seconds": int(end.timestamp()), "nanos": end.microsecond * 1000},
        )

        req = monitoring_v3.ListTimeSeriesRequest(
            name=self.parent,
            filter=request_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        results = self._client.list_time_series(request=req)
        return [normalize_gcm_series(s._pb) for s in results]

    def aggregate_metric_stats(
        self,
        metric_type: str,
        aggregation: AggregationKind = AggregationKind.AVERAGE,
        alignment: AlignmentPeriod = AlignmentPeriod.FIVE_MINUTES,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        filter_expression: Optional[str] = None,
        minutes: int = 60,
    ) -> AggregationResult:
        """Retrieve aggregated statistics for a metric over a time window."""
        start, end = default_time_window(minutes) if not (start_time and end_time) else (start_time, end_time)

        request_filter = f'metric.type = "{metric_type}"'
        if filter_expression:
            request_filter = f'{request_filter} AND {filter_expression}'

        interval = monitoring_v3.TimeInterval(
            start_time={"seconds": int(start.timestamp()), "nanos": start.microsecond * 1000},
            end_time={"seconds": int(end.timestamp()), "nanos": end.microsecond * 1000},
        )

        aggregation_cfg = build_aggregation_dict(aggregation, alignment)

        req = monitoring_v3.ListTimeSeriesRequest(
            name=self.parent,
            filter=request_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            aggregation=monitoring_v3.Aggregation(
                alignment_period={"seconds": int(alignment.value[:-1])},
                per_series_aligner=aggregation.value,
            ),
        )

        results = self._client.list_time_series(request=req)
        series_list = [normalize_gcm_series(s._pb) for s in results]

        summary = _compute_summary(series_list)

        return AggregationResult(
            metric_type=metric_type,
            aggregation=aggregation,
            alignment_period=alignment,
            series=series_list,
            summary=summary,
        )

    def filter_metric_dimensions(
        self,
        metric_type: str,
        dimensions: List[DimensionFilter],
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        minutes: int = 60,
    ) -> List[MetricSeries]:
        """Query metric data filtered by resource labels or dimensions."""
        start, end = default_time_window(minutes) if not (start_time and end_time) else (start_time, end_time)

        filter_parts = [f'metric.type = "{metric_type}"']
        for dim in dimensions:
            filter_parts.append(dim.to_gcm_fragment())

        request_filter = " AND ".join(filter_parts)

        interval = monitoring_v3.TimeInterval(
            start_time={"seconds": int(start.timestamp()), "nanos": start.microsecond * 1000},
            end_time={"seconds": int(end.timestamp()), "nanos": end.microsecond * 1000},
        )

        req = monitoring_v3.ListTimeSeriesRequest(
            name=self.parent,
            filter=request_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        results = self._client.list_time_series(request=req)
        return [normalize_gcm_series(s._pb) for s in results]

    def compare_metric_series(
        self,
        metric_type: str,
        filter_a: Optional[str] = None,
        filter_b: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        minutes: int = 60,
    ) -> MetricComparisonResult:
        """Compare metric values for two resources or dimension filters over the same window."""
        start, end = default_time_window(minutes) if not (start_time and end_time) else (start_time, end_time)

        series_a = self.query_metric_window(metric_type, start_time=start, end_time=end, filter_expression=filter_a, minutes=minutes)
        series_b = self.query_metric_window(metric_type, start_time=start, end_time=end, filter_expression=filter_b, minutes=minutes)

        combined_a = series_a[0] if series_a else MetricSeries(metric_type=metric_type, resource_type="", points=[])
        combined_b = series_b[0] if series_b else MetricSeries(metric_type=metric_type, resource_type="", points=[])

        delta_mean, delta_max, delta_min, correlation = _compute_comparison(combined_a, combined_b)

        return MetricComparisonResult(
            series_a=combined_a,
            series_b=combined_b,
            delta_mean=delta_mean,
            delta_max=delta_max,
            delta_min=delta_min,
            correlation=correlation,
        )


def _compute_summary(series_list: List[MetricSeries]) -> Dict[str, float]:
    """Compute summary statistics across all series."""
    all_values = [p.value for s in series_list for p in s.points]
    if not all_values:
        return {"count": 0, "mean": 0.0, "min": 0.0, "max": 0.0}
    return {
        "count": len(all_values),
        "mean": sum(all_values) / len(all_values),
        "min": min(all_values),
        "max": max(all_values),
    }


def _compute_comparison(
    a: MetricSeries, b: MetricSeries
) -> Tuple[float, float, float, Optional[float]]:
    """Compute delta and correlation between two metric series."""
    vals_a = [p.value for p in a.points]
    vals_b = [p.value for p in b.points]

    if not vals_a or not vals_b:
        return 0.0, 0.0, 0.0, None

    mean_a = sum(vals_a) / len(vals_a)
    mean_b = sum(vals_b) / len(vals_b)
    delta_mean = mean_a - mean_b

    delta_max = max(vals_a) - max(vals_b) if vals_a and vals_b else 0.0
    delta_min = min(vals_a) - min(vals_b) if vals_a and vals_b else 0.0

    # Pearson correlation
    n = min(len(vals_a), len(vals_b))
    if n < 2:
        return delta_mean, delta_max, delta_min, None

    a_trim = vals_a[:n]
    b_trim = vals_b[:n]
    mean_a_n = sum(a_trim) / n
    mean_b_n = sum(b_trim) / n

    cov = sum((a_trim[i] - mean_a_n) * (b_trim[i] - mean_b_n) for i in range(n)) / n
    std_a = (sum((x - mean_a_n) ** 2 for x in a_trim) / n) ** 0.5
    std_b = (sum((x - mean_b_n) ** 2 for x in b_trim) / n) ** 0.5

    if std_a == 0 or std_b == 0:
        correlation = None
    else:
        correlation = cov / (std_a * std_b)

    return delta_mean, delta_max, delta_min, correlation
