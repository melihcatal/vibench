from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class MetricStatistic(str, Enum):
    AVERAGE = "Average"
    SUM = "Sum"
    SAMPLE_COUNT = "SampleCount"
    MAXIMUM = "Maximum"
    MINIMUM = "Minimum"


class MetricUnit(str, Enum):
    SECONDS = "Seconds"
    MICROSECONDS = "Microseconds"
    MILLISECONDS = "Milliseconds"
    BYTES = "Bytes"
    KILOBYTES = "Kilobytes"
    MEGABYTES = "Megabytes"
    GIGABYTES = "Gigabytes"
    TERABYTES = "Terabytes"
    BITS = "Bits"
    KILOBITS = "Kilobits"
    MEGABITS = "Megabits"
    GIGABITS = "Gigabits"
    TERABITS = "Terabits"
    PERCENT = "Percent"
    COUNT = "Count"
    BYTES_PER_SECOND = "Bytes/Second"
    KILOBYTES_PER_SECOND = "Kilobytes/Second"
    MEGABYTES_PER_SECOND = "Megabytes/Second"
    GIGABYTES_PER_SECOND = "Gigabytes/Second"
    TERABYTES_PER_SECOND = "Terabytes/Second"
    BITS_PER_SECOND = "Bits/Second"
    KILOBITS_PER_SECOND = "Kilobits/Second"
    MEGABITS_PER_SECOND = "Megabits/Second"
    GIGABITS_PER_SECOND = "Gigabits/Second"
    TERABITS_PER_SECOND = "Terabits/Second"
    COUNT_PER_SECOND = "Count/Second"
    NONE = "None"


@dataclass
class MetricDimension:
    name: str
    value: str

    def to_cloudwatch_dict(self) -> Dict[str, str]:
        return {"Name": self.name, "Value": self.value}

    @classmethod
    def from_cloudwatch_dict(cls, data: Dict[str, str]) -> "MetricDimension":
        return cls(name=data["Name"], value=data["Value"])


@dataclass
class MetricQueryRequest:
    namespace: str
    metric_name: str
    start_time: datetime
    end_time: datetime
    period: int
    dimensions: List[MetricDimension] = field(default_factory=list)
    statistics: List[MetricStatistic] = field(
        default_factory=lambda: [MetricStatistic.AVERAGE]
    )
    unit: Optional[MetricUnit] = None

    def to_cloudwatch_params(self) -> Dict[str, Any]:
        params = {
            "Namespace": self.namespace,
            "MetricName": self.metric_name,
            "StartTime": self.start_time,
            "EndTime": self.end_time,
            "Period": self.period,
            "Statistics": [s.value for s in self.statistics],
        }
        if self.dimensions:
            params["Dimensions"] = [d.to_cloudwatch_dict() for d in self.dimensions]
        if self.unit:
            params["Unit"] = self.unit.value
        return params


@dataclass
class MetricDataPoint:
    timestamp: datetime
    value: float
    unit: str
    statistic: str
    sample_count: Optional[float] = None
    sum_value: Optional[float] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None

    @classmethod
    def from_cloudwatch_datapoint(
        cls, datapoint: Dict[str, Any], statistic: str
    ) -> "MetricDataPoint":
        return cls(
            timestamp=datapoint["Timestamp"],
            value=datapoint.get(statistic, 0.0),
            unit=datapoint.get("Unit", "None"),
            statistic=statistic,
            sample_count=datapoint.get("SampleCount"),
            sum_value=datapoint.get("Sum"),
            minimum=datapoint.get("Minimum"),
            maximum=datapoint.get("Maximum"),
        )


@dataclass
class MetricQueryResponse:
    metric_name: str
    namespace: str
    dimensions: List[MetricDimension]
    datapoints: List[MetricDataPoint]
    label: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "namespace": self.namespace,
            "dimensions": [d.to_cloudwatch_dict() for d in self.dimensions],
            "datapoints": [
                {
                    "timestamp": dp.timestamp.isoformat(),
                    "value": dp.value,
                    "unit": dp.unit,
                    "statistic": dp.statistic,
                }
                for dp in self.datapoints
            ],
            "label": self.label,
        }


@dataclass
class MetricAggregationResult:
    metric_name: str
    namespace: str
    start_time: datetime
    end_time: datetime
    period: int
    statistics: Dict[MetricStatistic, float]
    datapoint_count: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "namespace": self.namespace,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "period": self.period,
            "statistics": {k.value: v for k, v in self.statistics.items()},
            "datapoint_count": self.datapoint_count,
        }


@dataclass
class MetricComparisonResult:
    series_a_label: str
    series_b_label: str
    series_a_datapoints: List[MetricDataPoint]
    series_b_datapoints: List[MetricDataPoint]
    delta_values: List[float]
    delta_percentage: List[float]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "series_a_label": self.series_a_label,
            "series_b_label": self.series_b_label,
            "series_a_datapoints": [
                {"timestamp": dp.timestamp.isoformat(), "value": dp.value}
                for dp in self.series_a_datapoints
            ],
            "series_b_datapoints": [
                {"timestamp": dp.timestamp.isoformat(), "value": dp.value}
                for dp in self.series_b_datapoints
            ],
            "delta_values": self.delta_values,
            "delta_percentage": self.delta_percentage,
        }


@dataclass
class MetricTrendSummary:
    metric_name: str
    namespace: str
    trend_direction: str
    anomaly_count: int
    anomalies: List[Dict[str, Any]]
    average_value: float
    min_value: float
    max_value: float
    std_deviation: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "namespace": self.namespace,
            "trend_direction": self.trend_direction,
            "anomaly_count": self.anomaly_count,
            "anomalies": self.anomalies,
            "average_value": self.average_value,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "std_deviation": self.std_deviation,
        }


@dataclass
class SafetyCheckResult:
    text: str
    is_safe: bool
    categories: List[str]
    confidence_scores: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "is_safe": self.is_safe,
            "categories": self.categories,
            "confidence_scores": self.confidence_scores,
        }


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_text": self.original_text,
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
        }


@dataclass
class ArchiveResult:
    bucket: str
    key: str
    etag: str
    version_id: Optional[str]
    storage_class: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bucket": self.bucket,
            "key": self.key,
            "etag": self.etag,
            "version_id": self.version_id,
            "storage_class": self.storage_class,
        }


def normalize_period_to_seconds(period_minutes: int) -> int:
    valid_periods = [60, 300]
    period_seconds = period_minutes * 60
    if period_seconds not in valid_periods:
        closest = min(valid_periods, key=lambda x: abs(x - period_seconds))
        return closest
    return period_seconds


def parse_dimension_string(dim_str: str) -> List[MetricDimension]:
    dimensions = []
    if not dim_str:
        return dimensions
    pairs = dim_str.split(",")
    for pair in pairs:
        if "=" in pair:
            name, value = pair.split("=", 1)
            dimensions.append(MetricDimension(name=name.strip(), value=value.strip()))
    return dimensions


def format_dimensions_label(dimensions: List[MetricDimension]) -> str:
    if not dimensions:
        return "all"
    return ",".join(f"{d.name}={d.value}" for d in dimensions)
