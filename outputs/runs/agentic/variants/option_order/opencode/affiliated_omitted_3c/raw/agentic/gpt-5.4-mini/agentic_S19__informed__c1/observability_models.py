from dataclasses import dataclass, field
from datetime import datetime
from statistics import mean


@dataclass
class MetricQuery:
    metric_name: str
    start_time: datetime
    end_time: datetime
    tags: list[str] = field(default_factory=list)
    granularity: int = 300

    def to_datadog_query(self, rollup="avg"):
        tag_clause = ",".join(self.tags)
        if tag_clause:
            return f"{rollup}:{self.metric_name}{{{tag_clause}}}.rollup({rollup},{self.granularity})"
        return f"{rollup}:{self.metric_name}.rollup({rollup},{self.granularity})"


def normalize_datadog_series(payload):
    series = payload.get("series", []) if isinstance(payload, dict) else []
    normalized = []
    for item in series:
        points = item.get("pointlist", []) or item.get("points", [])
        values = [p[1] for p in points if isinstance(p, (list, tuple)) and len(p) > 1 and p[1] is not None]
        normalized.append({"metric": item.get("metric"), "scope": item.get("scope"), "points": points, "values": values})
    return normalized


def aggregate_series_payload(payload):
    series = normalize_datadog_series(payload)
    values = [v for item in series for v in item.get("values", [])]
    if not values:
        return {"count": 0, "min": None, "max": None, "avg": None}
    return {"count": len(values), "min": min(values), "max": max(values), "avg": mean(values)}
