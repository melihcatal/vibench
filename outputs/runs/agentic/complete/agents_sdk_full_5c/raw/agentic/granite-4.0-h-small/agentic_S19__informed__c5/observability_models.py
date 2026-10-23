from typing import Dict, Any, List

class MetricQueryRequest:
    """Normalization object for building monitoring metric queries."""
    def __init__(self, metric: str, start_time: float, end_time: float, filter_expr: str = None, aggregation: str = None):
        self.metric = metric        # full metric type string, e.g. 'compute.googleapis.com/instance/cpu/utilization'
        self.start_time = start_time
        self.end_time = end_time
        self.filter_expr = filter_expr
        self.aggregation = aggregation

    def to_dict(self):
        """Convert to a dict usable by the ObservabilityClient."""
        interval = {
            'start_time': {'seconds': int(self.start_time)},
            'end_time': {'seconds': int(self.end_time)}
        }
        return {
            'metric': self.metric,
            'filter_expr': self.filter_expr,
            'interval': interval,
            'aggregation': self.aggregation
        }


class MetricResponse:
    """Thin wrapper around raw API response for standardization."""
    def __init__(self, raw_response: List[Any]):
        self.raw = raw_response
        self.samples = self._extract_samples()

    def _extract_samples(self):
        samples = []
        for point in self.raw:
            # Convert Google's Point namedtuple to a dict
            samples.append({
                'interval': {
                    'start': point.interval.start_time.seconds,
                    'end': point.interval.end_time.seconds
                },
                'value': point.value.double_value if point.value else None
            })
        return samples

    def to_dataframe(self):
        """Placeholder for future pandas conversion."""
        raise NotImplementedError('Conversion to pandas DataFrame not implemented')


class MetricComparisonResult:
    """Container for comparing two metric series (e.g., different resources)."""
    def __init__(self, series_a, series_b):
        self.series_a = series_a  # list of MetricResponse objects for filter_a
        self.series_b = series_b  # list of MetricResponse objects for filter_b

    def delta_summary(self):
        """Simple point‑wise delta if series have identical timestamps."""
        # Ensure both series have same length and aligned timestamps
        if len(self.series_a) != len(self.series_b):
            raise ValueError('Series length mismatch')
        deltas = []
        for a, b in zip(self.series_a, self.series_b):
            val_a = a['samples'][0]['value'] if a['samples'] else None
            val_b = b['samples'][0]['value'] if b['samples'] else None
            deltas.append(val_b - val_a if val_a is not None and val_b is not None else None)
        return deltas
