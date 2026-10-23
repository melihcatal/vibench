
"""
Local request, response, and normalization helpers for Managed Metrics Monitoring.
"""

class MetricRequest:
    """
    Represents a request to send metrics.
    """
    def __init__(self, metric_name: str, value: float, timestamp: int, dimensions: dict = None):
        self.metric_name = metric_name
        self.value = value
        self.timestamp = timestamp
        self.dimensions = dimensions if dimensions is not None else {}

    def to_dict(self):
        return {
            "metric_name": self.metric_name,
            "value": self.value,
            "timestamp": self.timestamp,
            "dimensions": self.dimensions
        }

class MetricResponse:
    """
    Represents a response from a metric ingestion service.
    """
    def __init__(self, success: bool, message: str = None, error: str = None):
        self.success = success
        self.message = message
        self.error = error

    def to_dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "error": self.error
        }

def normalize_metric_data(data: dict) -> MetricRequest:
    """
    Normalizes raw data into a MetricRequest object.
    This is a placeholder for actual normalization logic.
    """
    # Example of expected input data:
    # {
    #     "name": "cpu_usage",
    #     "val": 0.75,
    #     "ts": 1678886400,
    #     "tags": {"host": "server1", "region": "us-east-1"}
    # }
    metric_name = data.get("name") or data.get("metric_name")
    value = data.get("val") or data.get("value")
    timestamp = data.get("ts") or data.get("timestamp")
    dimensions = data.get("tags") or data.get("dimensions")

    if not all([metric_name, value, timestamp]):
        raise ValueError("Missing required fields for metric normalization: name, value, timestamp")

    return MetricRequest(
        metric_name=str(metric_name),
        value=float(value),
        timestamp=int(timestamp),
        dimensions=dimensions
    )
