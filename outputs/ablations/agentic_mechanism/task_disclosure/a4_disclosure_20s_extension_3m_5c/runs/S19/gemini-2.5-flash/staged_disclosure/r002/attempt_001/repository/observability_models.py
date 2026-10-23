
class ManagedMetricsRequest:
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

class ManagedMetricsResponse:
    def __init__(self, success: bool, message: str = None):
        self.success = success
        self.message = message

    def to_dict(self):
        return {
            "success": self.success,
            "message": self.message
        }

def normalize_metric_data(data: dict) -> ManagedMetricsRequest:
    # Example normalization: ensure required fields are present and correctly typed
    if not all(k in data for k in ["metric_name", "value", "timestamp"]):
        raise ValueError("Missing required fields in metric data")

    metric_name = str(data["metric_name"])
    value = float(data["value"])
    timestamp = int(data["timestamp"])
    dimensions = data.get("dimensions", {})

    return ManagedMetricsRequest(metric_name, value, timestamp, dimensions)
