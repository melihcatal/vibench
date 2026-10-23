from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class AggregationType(Enum):
    AVG = "avg"
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    P50 = "p50"
    P90 = "p90"
    P95 = "p95"
    P99 = "p99"


class MetricType(Enum):
    GAUGE = "gauge"
    RATE = "rate"
    COUNT = "count"


@dataclass
class MetricQueryRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    aggregation: AggregationType = AggregationType.AVG
    interval_seconds: int = 300
    dimensions: dict[str, str] = field(default_factory=dict)
    group_by: list[str] = field(default_factory=list)

    def to_datadog_query(self) -> str:
        parts = [self.metric_name]
        for key, value in sorted(self.dimensions.items()):
            parts.append(f"{key}:{value}")
        return " ".join(parts)

    def to_datadog_query_params(self) -> dict[str, Any]:
        return {
            "from": int(self.start_time.timestamp()),
            "to": int(self.end_time.timestamp()),
            "query": self.to_datadog_query(),
            "aggregation": self.aggregation.value,
        }


@dataclass
class MetricDataPoint:
    timestamp: datetime
    value: float
    dimensions: dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeries:
    metric_name: str
    aggregation: str
    dimensions: dict[str, str]
    points: list[MetricDataPoint]

    def values(self) -> list[float]:
        return [p.value for p in self.points]

    def timestamps(self) -> list[datetime]:
        return [p.timestamp for p in self.points]


@dataclass
class MetricAggregatedStats:
    metric_name: str
    aggregation: str
    start_time: datetime
    end_time: datetime
    avg: float
    min: float
    max: float
    sum: float
    count: int
    p50: float
    p90: float
    p95: float
    p99: float


@dataclass
class MetricComparisonResult:
    series_a: MetricSeries
    series_b: MetricSeries
    diff_avg: float
    diff_max: float
    diff_min: float
    correlation: float


@dataclass
class MetricAnomaly:
    timestamp: datetime
    value: float
    expected_value: float
    deviation: float
    severity: str


@dataclass
class MetricSummary:
    metric_name: str
    period_start: datetime
    period_end: datetime
    overall_avg: float
    overall_max: float
    overall_min: float
    trend_direction: str
    anomalies: list[MetricAnomaly]
    series: MetricSeries


@dataclass
class SafetyCheckResult:
    text: str
    is_safe: bool
    flagged_categories: list[str]
    confidence: float
    details: str


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_locale: str
    target_locale: str
    model_used: str


@dataclass
class ArchiveResult:
    archive_key: str
    bucket: str
    size_bytes: int
    checksum: str
    timestamp: datetime


def normalize_datadog_series(
    raw_series: dict, metric_name: str, aggregation: str
) -> MetricSeries:
    dimensions = {}
    if "scope" in raw_series:
        scope = raw_series["scope"]
        for tag in scope.split(","):
            if ":" in tag:
                k, v = tag.split(":", 1)
                dimensions[k.strip()] = v.strip()

    points = []
    for dp in raw_series.get("pointlist", []):
        if dp[1] is not None:
            points.append(
                MetricDataPoint(
                    timestamp=datetime.utcfromtimestamp(dp[0] / 1000.0),
                    value=float(dp[1]),
                    dimensions=dict(dimensions),
                )
            )

    return MetricSeries(
        metric_name=metric_name,
        aggregation=aggregation,
        dimensions=dimensions,
        points=points,
    )


def compute_percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    k = (len(sorted_vals) - 1) * (percentile / 100.0)
    f = int(k)
    c = f + 1
    if c >= len(sorted_vals):
        return sorted_vals[f]
    return sorted_vals[f] + (k - f) * (sorted_vals[c] - sorted_vals[f])


def compute_correlation(xs: list[float], ys: list[float]) -> float:
    n = min(len(xs), len(ys))
    if n < 2:
        return 0.0
    xs = xs[:n]
    ys = ys[:n]
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    cov = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n)) / n
    std_x = (sum((x - mean_x) ** 2 for x in xs) / n) ** 0.5
    std_y = (sum((y - mean_y) ** 2 for y in ys) / n) ** 0.5
    if std_x == 0 or std_y == 0:
        return 0.0
    return cov / (std_x * std_y)


def detect_anomalies(
    series: MetricSeries, sigma_threshold: float = 2.0
) -> list[MetricAnomaly]:
    values = series.values()
    if len(values) < 3:
        return []
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    std = variance**0.5
    if std == 0:
        return []
    anomalies = []
    for point in series.points:
        deviation = abs(point.value - mean) / std
        if deviation > sigma_threshold:
            severity = (
                "high" if deviation > 3.0 else "medium" if deviation > 2.5 else "low"
            )
            anomalies.append(
                MetricAnomaly(
                    timestamp=point.timestamp,
                    value=point.value,
                    expected_value=mean,
                    deviation=deviation,
                    severity=severity,
                )
            )
    return anomalies
