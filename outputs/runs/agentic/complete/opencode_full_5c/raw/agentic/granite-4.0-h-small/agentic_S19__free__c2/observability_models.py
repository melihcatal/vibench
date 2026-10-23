# [HELPER] observability_models.py

from typing import Optional, List, Dict, Any

# Request models

class MetricQueryRequest:
    metric: str
    start: str  # RFC3339 timestamp
    end: str    # RFC3339 timestamp
    filter: Optional[str] = None
    aggregation: Optional[str] = None

    def __init__(self, metric, start, end, **kwargs):
        self.metric = metric
        self.start = start
        self.end = end
        for k, v in kwargs.items():
            setattr(self, k, v)

# Response models

class MetricQueryResponse:
    series: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None

    def __init__(self, series, metadata=None):
        self.series = series
        self.metadata = metadata

# Util models for downstream steps

class MetricStatsRequest:
    metric: str
    start: str
    end: str
    granularity: Optional[str] = None
    filter: Optional[str] = None

    def __init__(self, metric, start, end, **kwargs):
        self.metric = metric
        self.start = start
        self.end = end
        for k, v in kwargs.items():
            setattr(self, k, v)

# Normalization helpers

def normalize_series(raw_series):
    \"\"\"Convert monitoring_v3.TimeSeries objects to simple dicts.\"\"\"
    normalized = []
    for ts in raw_series:
        # Pull metric, metric kind, resource, and points
        series_dict = {
            "metric": ts.metric.type,
            "resource": ts.resource.type,
            "points": [pt.to_dict() for pt in ts.points],
        }
        normalized.append(series_dict)
    return normalized

# Example usage shown for downstream steps (not executed here)
# def example_summarize(raw):\n#     series = normalize_series(raw)\n#     # aggregate, detect anomalies, etc.\n#     return series\n