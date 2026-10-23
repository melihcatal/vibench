from typing import Dict, Any, List

class MetricQueryRequest:
    def __init__(self, namespace: str, metric_name: str, start: str, end: str, period: int = 60):
        self.namespace = namespace
        self.metric_name = metric_name
        self.start = start  # ISO8601 string
        self.end = end
        self.period = period
        self.statistics: List[str] = []
        self.dimensions: List[Dict[str, str]] = []

    def to_boto_params(self) -> Dict[str, Any]:
        params = {
            "Namespace": self.namespace,
            "MetricName": self.metric_name,
            "StartTime": self.start,
            "EndTime": self.end,
            "Period": self.period,
        }
        if self.statistics:
            params["Statistics"] = self.statistics
        if self.dimensions:
            params["Dimensions"] = self.dimensions
        return params


class MetricQueryResponse:
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        self.datapoints: List[Dict[str, Any]] = raw.get("Datapoints", [])
        self.label = raw.get("Label")

    def as_dataframe(self):
        """Placeholder for converting datapoints to pandas DataFrame."""
        # In real code you could return pd.DataFrame(self.datapoints)
        return self.datapoints


class MetricStatisticsRequest(MetricQueryRequest):
    """Same payload as Query, but focused on statistical aggregation."""
    pass


class MetricStatisticsResponse(MetricQueryResponse):
    pass


class MetricFilterRequest(MetricQueryRequest):
    """Request payload for filtering by dimensions."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limit: int = 100


class MetricFilterResponse:
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        self.datapoints = raw.get("Datapoints", [])
        self.labels = raw.get("Labels", [])


class MetricSeriesRequest(MetricFilterRequest):
    """Request for comparing two series; extends dimension filtering."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.namespace_b: str = None
        self.dimensions_b: List[Dict[str, str]] = []

    def set_namespace_b(self, ns: str):
        self.namespace_b = ns

    def set_dimensions_b(self, dims: List[Dict[str, str]]):
        self.dimensions_b = dims


class MetricSeriesResponse:
    def __init__(self, raw_a: Dict[str, Any], raw_b: Dict[str, Any]):
        self.series_a = MetricQueryResponse(raw_a)
        self.series_b = MetricQueryResponse(raw_b)

    def compare(self):
        """Return a simple diff summary."""
        a = self.series_a.datapoints
        b = self.series_b.datapoints
        # Example diff: count difference
        diff = len(a) - len(b)
        return {
            "datapoint_count_diff": diff,
            "metric_a_label": self.series_a.label,
            "metric_b_label": self.series_b.label,
        }
