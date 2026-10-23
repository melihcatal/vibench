from __future__ import annotations

import time
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class MetricQueryRequest:
    metric: str
    start_ts: int
    end_ts: int
    aggregation: str = "avg"
    rollup: str = "avg"
    interval: int = 300
    tag_filters: list[str] = field(default_factory=list)

    def to_payload(self) -> dict[str, Any]:
        query_parts = [f"{self.aggregation}:{self.metric}"]
        if self.tag_filters:
            tag_clause = ",".join(self.tag_filters)
            query_parts.append(f"{{{tag_clause}}}")
        return {
            "query": " ".join(query_parts),
            "from": self.start_ts,
            "to": self.end_ts,
            "rollup": True,
            "rollup_interval": self.interval,
            "rollup_method": self.rollup,
        }


@dataclass
class Datapoint:
    timestamp: int
    value: float


@dataclass
class MetricSeries:
    metric: str
    expression: str
    scope: str
    aggregation: str
    points: list[Datapoint] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric": self.metric,
            "expression": self.expression,
            "scope": self.scope,
            "aggregation": self.aggregation,
            "points": [{"ts": p.timestamp, "value": p.value} for p in self.points],
        }


@dataclass
class MetricQueryResponse:
    series: list[MetricSeries]
    query: str
    from_ts: int
    to_ts: int
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "series": [s.to_dict() for s in self.series],
            "query": self.query,
            "from_ts": self.from_ts,
            "to_ts": self.to_ts,
            "message": self.message,
        }


@dataclass
class AggregatedStats:
    metric: str
    aggregation: str
    start_ts: int
    end_ts: int
    count: int
    avg: float
    min: float
    max: float
    sum: float
    p50: float = 0.0
    p90: float = 0.0
    p99: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DimensionFilter:
    key: str
    value: str
    operator: str = "="

    def to_tag_string(self) -> str:
        if self.operator == "!=":
            return f"{self.key}:!{self.value}"
        return f"{self.key}:{self.value}"


@dataclass
class MetricComparisonRequest:
    metric: str
    start_ts: int
    end_ts: int
    series_a_tags: list[str]
    series_b_tags: list[str]
    aggregation: str = "avg"
    interval: int = 300

    def to_queries(self) -> list[dict[str, Any]]:
        queries = []
        for tags in (self.series_a_tags, self.series_b_tags):
            tag_clause = ",".join(tags) if tags else "*"
            query_str = f"{self.aggregation}:{self.metric}{{{tag_clause}}}"
            queries.append(
                {
                    "query": query_str,
                    "from": self.start_ts,
                    "to": self.end_ts,
                    "rollup": True,
                    "rollup_interval": self.interval,
                    "rollup_method": self.aggregation,
                }
            )
        return queries


@dataclass
class MetricComparisonResponse:
    series_a: MetricSeries
    series_b: MetricSeries
    metric: str
    start_ts: int
    end_ts: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_a": self.series_a.to_dict(),
            "series_b": self.series_b.to_dict(),
            "metric": self.metric,
            "start_ts": self.start_ts,
            "end_ts": self.end_ts,
        }


def now_epoch() -> int:
    return int(time.time())


def epoch_minutes_ago(minutes: int) -> int:
    return now_epoch() - (minutes * 60)
