"""
Data models and normalization helpers for Datadog Metrics Monitoring responses.

Defines request/response structures and provides utilities for parsing
and normalizing Datadog metric data into consistent application formats.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class MetricQueryRequest:
    """Request model for querying Datadog metrics."""
    metric: str
    from_ts: int
    to_ts: int
    aggregator: str = "avg"
    rollup: int = 60
    tag_filters: Optional[list[str]] = None

    def to_datadog_query_params(self) -> dict[str, Any]:
        """Convert to Datadog v1 query API parameters."""
        params = {
            "query": self.metric,
            "from": self.from_ts,
            "to": self.to_ts,
        }
        if self.aggregator:
            params["aggregator"] = self.aggregator
        return params

    def to_datadog_v2_payload(self) -> dict[str, Any]:
        """Convert to Datadog v2 query payload format."""
        data: dict[str, Any] = {
            "data": {
                "attributes": {
                    "query": {
                        "formulas": [{"formula": "a"}],
                        "queries": [{
                            "name": "a",
                            "data_source": "metrics",
                            "query": self.metric,
                            "aggregator": self.aggregator,
                            "group_by": [],
                        }],
                    },
                    "from_ts": self.from_ts,
                    "to_ts": self.to_ts,
                },
            },
        }
        if self.tag_filters:
            tag_list = self.tag_filters
            data["data"]["attributes"]["query"]["queries"][0]["tags"] = tag_list
        return data


@dataclass
class MetricDataPoint:
    """Represents a single metric datapoint."""
    timestamp: datetime
    value: float
    tags: dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeries:
    """Represents a complete metric time series."""
    metric: str
    points: list[MetricDataPoint] = field(default_factory=list)
    display_name: str = ""
    unit: str = ""
    tag_set: dict[str, str] = field(default_factory=dict)

    @property
    def count(self) -> int:
        return len(self.points)

    @property
    def values(self) -> list[float]:
        return [p.value for p in self.points]

    @property
    def timestamps(self) -> list[datetime]:
        return [p.timestamp for p in self.points]


@dataclass
class MetricAggregation:
    """Aggregated statistics for a metric series."""
    metric: str
    avg: float
    min_val: float
    max_val: float
    sum_val: float
    count: int
    percentiles: dict[str, float] = field(default_factory=dict)
    tag_set: dict[str, str] = field(default_factory=dict)


@dataclass
class MetricComparison:
    """Comparison results between two metric series."""
    series_a: MetricSeries
    series_b: MetricSeries
    delta_avg: float
    delta_max: float
    delta_min: float
    correlation: float = 0.0
    overlap_pct: float = 0.0


def parse_datadog_query_response(response_data: dict[str, Any]) -> list[MetricSeries]:
    """
    Parse a Datadog v1 query API response into MetricSeries objects.

    Response format:
    {
      "series": [
        {
          "metric": "metric.name",
          "pointlist": [[timestamp_ms, value], ...],
          "tag_set": ["key:value", ...],
          "display_name": "...",
          "unit": "..."
        }
      ]
    }
    """
    series_list = response_data.get("series", [])
    result = []
    for raw_series in series_list:
        metric_name = raw_series.get("metric", "")
        pointlist = raw_series.get("pointlist", [])
        raw_tags = raw_series.get("tag_set", [])
        tag_dict = {}
        for tag_str in raw_tags:
            if ":" in tag_str:
                k, v = tag_str.split(":", 1)
                tag_dict[k] = v
        points = []
        for ts_ms, val in pointlist:
            points.append(MetricDataPoint(
                timestamp=datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc),
                value=float(val) if val is not None else 0.0,
            ))
        series = MetricSeries(
            metric=metric_name,
            points=points,
            display_name=raw_series.get("display_name", metric_name),
            unit=raw_series.get("unit", ""),
            tag_set=tag_dict,
        )
        result.append(series)
    return result


def parse_datadog_v2_query_response(response_data: dict[str, Any]) -> list[MetricSeries]:
    """Parse a Datadog v2 query API response into MetricSeries objects."""
    data = response_data.get("data", {})
    attrs = data.get("attributes", {})
    series_data = attrs.get("series", [])
    result = []
    for raw_series in series_data:
        metric_name = raw_series.get("metric", "")
        group = raw_series.get("group", {})
        points = []
        for raw_point in raw_series.get("values", []):
            ts = raw_point.get("timestamp", 0)
            val = raw_point.get("value")
            if val is not None:
                points.append(MetricDataPoint(
                    timestamp=datetime.fromtimestamp(ts, tz=timezone.utc),
                    value=float(val),
                ))
        series = MetricSeries(
            metric=metric_name,
            points=points,
            tag_set=group,
        )
        result.append(series)
    return result


def compute_aggregation(series: MetricSeries) -> MetricAggregation:
    """Compute aggregate statistics from a MetricSeries."""
    values = series.values
    if not values:
        return MetricAggregation(
            metric=series.metric,
            avg=0.0, min_val=0.0, max_val=0.0,
            sum_val=0.0, count=0, tag_set=series.tag_set,
        )
    return MetricAggregation(
        metric=series.metric,
        avg=sum(values) / len(values),
        min_val=min(values),
        max_val=max(values),
        sum_val=sum(values),
        count=len(values),
        tag_set=series.tag_set,
    )
