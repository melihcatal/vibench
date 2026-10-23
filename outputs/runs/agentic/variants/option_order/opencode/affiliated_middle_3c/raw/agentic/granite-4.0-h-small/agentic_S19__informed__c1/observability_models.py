# [HELPER] observability_models.py

# Request/response normalization helpers for Managed Metrics Monitoring

class MetricQueryRequest:
    """Base class for metric query payloads.
    Attributes:
        metric_name: str - name of the metric
        start_time: int - epoch ms start
        end_time: int - epoch ms end
        granularity_ms: int - query granularity
        resources: list - resource identifiers (labels, dimensions, etc.)
    """
    def __init__(self, metric_name, start_time, end_time, granularity_ms, resources=None):
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time
        self.granularity_ms = granularity_ms
        self.resources = resources or []

    def normalize(self):
        """Convert to provider-specific format (placeholder)."""
        return {
            'metric': self.metric_name,
            'start': self.start_time,
            'end': self.end_time,
            'granularity': self.granularity_ms,
            'resources': self.resources
        }

# Simple response wrapper used across implementations
class MetricResponse:
    """Normalized response data from any provider.
    Attributes:
        datapoints: list - list of (timestamp, value) pairs
        metadata: dict - optional provider-specific metadata
    """
    def __init__(self, datapoints, metadata=None):
        self.datapoints = datapoints
        self.metadata = metadata or {}

    @classmethod
    def from_provider(cls, provider_data):
        """Create an instance from a provider-specific raw response.",
        raise NotImplementedError
