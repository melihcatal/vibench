# observability_models.py

class MetricQueryRequest:
    """Normalized request container for a metric query."""
    def __init__(self, Namespace: str, MetricName: str, StartTime: str, EndTime: str, Period: int = 60, Statistics: list = None):
        self.Namespace = Namespace
        self.MetricName = MetricName
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.Period = Period
        self.Statistics = Statistics or []

class MetricQueryResponse:
    """Normalized response container for metric data points."""
    def __init__(self, Datapoints: list):
        self.Datapoints = Datapoints


class MetricStatsRequest(MetricQueryRequest):
    """Request container specific to aggregated statistics."""
    pass

class MetricStatsResponse:
    """Response container for aggregated statistics."""
    def __init__(self, Timestamps: list, Values: dict):
        self.Timestamps = Timestamps
        self.Values = Values


class MetricFilterRequest:
    """Request container for filtered metric queries."""
    def __init__(self, Namespace: str, MetricName: str, StartTime: str, EndTime: str, Dimensions: dict):
        self.Namespace = Namespace
        self.MetricName = MetricName
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.Dimensions = Dimensions

class MetricFilterResponse:
    """Response container for filtered metric queries."""
    def __init__(self, Datapoints: list):
        self.Datapoints = Datapoints


class CompareMetricRequest:
    """Request container for side‑by‑side metric comparison."""
    def __init__(self, Namespace: str, MetricName: str, StartTime: str, EndTime: str, DimensionFilters: list):
        self.Namespace = Namespace
        self.MetricName = MetricName
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.DimensionFilters = DimensionFilters

class CompareMetricResponse:
    """Response container for metric comparison results."""
    def __init__(self, Comparison: dict):
        self.Comparison = Comparison


class MetricSummary:
    """Helper to summarize trends or anomalies from metric data."""
    @staticmethod
    def summarize(datapoints: list) -> dict:
        """Produce a simple summary: count, avg, min, max, recent trend."""
        values = [dp['Value'] for dp in datapoints]
        return {
            'count': len(values),
            'average': sum(values) / len(values) if values else None,
            'min': min(values) if values else None,
            'max': max(values) if values else None,
            'trend': 'stable' if len(values) >= 2 and max(values) - min(values) < 5 else 'fluctuating'
        }
