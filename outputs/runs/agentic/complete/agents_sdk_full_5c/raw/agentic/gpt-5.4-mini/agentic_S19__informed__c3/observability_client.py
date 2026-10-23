from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Iterable

import boto3
from botocore.config import Config

from observability_models import MetricSeriesPoint, MetricSeriesResult, MetricStatsResult, normalize_dimensions


@dataclass(slots=True)
class ObservabilityConfig:
    region_name: str | None = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    namespace: str = os.getenv("OBSERVABILITY_NAMESPACE", "Custom/Observability")
    default_period: int = int(os.getenv("OBSERVABILITY_PERIOD_SECONDS", "60"))


class ObservabilityClient:
    def __init__(self, config: ObservabilityConfig | None = None) -> None:
        self.config = config or ObservabilityConfig()
        self._client = boto3.client("cloudwatch", config=Config(retries={"max_attempts": 3}), region_name=self.config.region_name)

    def query_series(self, metric_name: str, start_time, end_time, dimensions: dict[str, str] | None = None, period: int | None = None, statistic: str = "Average") -> MetricSeriesResult:
        kwargs: dict[str, Any] = {
            "Namespace": self.config.namespace,
            "MetricName": metric_name,
            "StartTime": start_time,
            "EndTime": end_time,
            "Period": period or self.config.default_period,
            "Statistics": [statistic],
        }
        dims = normalize_dimensions(dimensions)
        if dims:
            kwargs["Dimensions"] = [{"Name": k, "Value": v} for k, v in dims.items()]
        response = self._client.get_metric_statistics(**kwargs)
        datapoints = sorted(response.get("Datapoints", []), key=lambda p: p["Timestamp"])
        points = [MetricSeriesPoint(timestamp=dp["Timestamp"], value=float(dp.get(statistic, 0.0)), unit=dp.get("Unit"), dimensions=dims) for dp in datapoints]
        return MetricSeriesResult(metric_name=metric_name, points=points)

    def get_statistics(self, metric_name: str, start_time, end_time, dimensions: dict[str, str] | None = None, period: int | None = None) -> MetricStatsResult:
        series = self.query_series(metric_name, start_time, end_time, dimensions=dimensions, period=period)
        values = [p.value for p in series.points]
        if not values:
            return MetricStatsResult(metric_name=metric_name)
        return MetricStatsResult(metric_name=metric_name, minimum=min(values), maximum=max(values), average=sum(values) / len(values), sum=sum(values), sample_count=float(len(values)))

    def compare_series(self, metric_name: str, left_dimensions: dict[str, str], right_dimensions: dict[str, str], start_time, end_time, period: int | None = None) -> tuple[MetricSeriesResult, MetricSeriesResult]:
        left = self.query_series(metric_name, start_time, end_time, dimensions=left_dimensions, period=period)
        right = self.query_series(metric_name, start_time, end_time, dimensions=right_dimensions, period=period)
        return left, right

    def archive_bytes(self, bucket: str, object_key: str, payload: bytes, content_type: str = "application/octet-stream") -> dict[str, Any]:
        s3 = boto3.client("s3", config=Config(retries={"max_attempts": 3}), region_name=self.config.region_name)
        return s3.put_object(Bucket=bucket, Key=object_key, Body=payload, ContentType=content_type)
