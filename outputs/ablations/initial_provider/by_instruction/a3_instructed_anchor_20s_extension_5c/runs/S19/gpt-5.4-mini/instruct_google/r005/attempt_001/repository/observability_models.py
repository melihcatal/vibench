from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class MetricWindow:
    metric_type: str
    minutes: int = 60
    resource_type: str | None = None
    filter_expression: str | None = None


@dataclass
class MetricPoint:
    timestamp: datetime
    value: float


def normalize_timestamp(value: datetime | str) -> datetime:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc)
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def normalize_value(value: object) -> float:
    if hasattr(value, "double_value"):
        return float(value.double_value)
    if hasattr(value, "int64_value"):
        return float(value.int64_value)
    if hasattr(value, "distribution_value"):
        return float(value.distribution_value.count)
    return float(value)
