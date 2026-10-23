
class MetricRequest:
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
    def __init__(self, status: str, message: str, metric_id: str = None):
        self.status = status
        self.message = message
        self.metric_id = metric_id

    def to_dict(self):
        return {
            "status": self.status,
            "message": self.message,
            "metric_id": self.metric_id
        }

def normalize_metric_data(data: dict) -> dict:
    """
    Normalizes metric data to a standard format.
    This is a placeholder for actual normalization logic.
    """
    normalized_data = {
        "name": data.get("metric_name"),
        "value": float(data.get("value")),
        "timestamp": int(data.get("timestamp")),
        "labels": data.get("dimensions", {})
    }
    return normalized_data
