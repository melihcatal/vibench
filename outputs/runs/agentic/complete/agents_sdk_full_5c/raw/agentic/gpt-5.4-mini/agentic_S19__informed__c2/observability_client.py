from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

import boto3

from observability_models import MetricDatapoint, MetricQuery, MetricSeries, MetricStats, isoformat, normalize_points, parse_datetime


@dataclass
class ObservabilityConfig:
    namespace: str
    region_name: str
    metrics_host: str = ""


class CloudWatchMetricsClient:
    def __init__(self, namespace: Optional[str] = None, region_name: Optional[str] = None) -> None:
        self.namespace = namespace or os.getenv("CLOUDWATCH_NAMESPACE", "ManagedMetrics")
        self.region_name = region_name or os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
        self._client = boto3.client("cloudwatch", region_name=self.region_name)

    def list_metric_series(self, metric_name: str, dimensions: Optional[Dict[str, str]] = None) -> List[MetricSeries]:
        dimensions = dimensions or {}
        response = self._client.list_metrics(
            Namespace=self.namespace,
            MetricName=metric_name,
            Dimensions=[{"Name": k, "Value": v} for k, v in dimensions.items()] if dimensions else [],
        )
        series: List[MetricSeries] = []
        for metric in response.get("Metrics", []):
            dims = {d["Name"]: d["Value"] for d in metric.get("Dimensions", [])}
            series.append(MetricSeries(metric_name=metric_name, dimensions=dims))
        return series

    def query_metric_window(self, query: MetricQuery) -> MetricSeries:
        response = self._client.get_metric_statistics(
            Namespace=self.namespace,
            MetricName=query.metric_name,
            Dimensions=[{"Name": k, "Value": v} for k, v in query.dimensions.items()],
            StartTime=query.start_time,
            EndTime=query.end_time,
            Period=query.granularity or 60,
            Statistics=["Average", "Sum", "Minimum", "Maximum", "SampleCount"],
        )
        datapoints = []
        for point in response.get("Datapoints", []):
            timestamp = point.get("Timestamp")
            if isinstance(timestamp, str):
                timestamp = parse_datetime(timestamp)
            datapoints.append(
                MetricDatapoint(
                    timestamp=timestamp,
                    value=float(point.get("Average", point.get("Sum", 0.0))),
                    dimensions=dict(query.dimensions),
                )
            )
        datapoints.sort(key=lambda p: p.timestamp)
        return MetricSeries(metric_name=query.metric_name, datapoints=datapoints, dimensions=dict(query.dimensions))

    def aggregate_metric_stats(self, query: MetricQuery) -> MetricStats:
        response = self._client.get_metric_statistics(
            Namespace=self.namespace,
            MetricName=query.metric_name,
            Dimensions=[{"Name": k, "Value": v} for k, v in query.dimensions.items()],
            StartTime=query.start_time,
            EndTime=query.end_time,
            Period=query.granularity or 60,
            Statistics=["Average", "Sum", "Minimum", "Maximum", "SampleCount"],
        )
        datapoints = response.get("Datapoints", [])
        minimum = min((float(p.get("Minimum")) for p in datapoints if "Minimum" in p), default=None)
        maximum = max((float(p.get("Maximum")) for p in datapoints if "Maximum" in p), default=None)
        average = None
        sum_ = None
        count = 0
        if datapoints:
            sum_values = [float(p.get("Sum", p.get("Average", 0.0))) for p in datapoints]
            sample_counts = [int(p.get("SampleCount", 1)) for p in datapoints]
            sum_ = float(sum(sum_values))
            count = int(sum(sample_counts))
            average = sum_ / count if count else None
        return MetricStats(
            metric_name=query.metric_name,
            start_time=query.start_time,
            end_time=query.end_time,
            minimum=minimum,
            maximum=maximum,
            average=average,
            sum=sum_,
            count=count,
        )

    def filter_metric_dimensions(self, metric_name: str, dimensions: Dict[str, str], start_time: datetime, end_time: datetime, period: int = 60) -> MetricSeries:
        return self.query_metric_window(MetricQuery(metric_name=metric_name, start_time=start_time, end_time=end_time, dimensions=dimensions, granularity=period))

    def compare_metric_series(self, metric_name: str, left_dimensions: Dict[str, str], right_dimensions: Dict[str, str], start_time: datetime, end_time: datetime, period: int = 60) -> Dict[str, MetricSeries]:
        left = self.filter_metric_dimensions(metric_name, left_dimensions, start_time, end_time, period)
        right = self.filter_metric_dimensions(metric_name, right_dimensions, start_time, end_time, period)
        return {"left": left, "right": right}
