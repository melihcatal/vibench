
class LogRequest:
    """Represents a log ingestion request."""
    def __init__(self, log_entry: dict):
        self.log_entry = log_entry

class LogResponse:
    """Represents a log ingestion response."""
    def __init__(self, status: str, message: str):
        self.status = status
        self.message = message

class LogNormalizer:
    """Provides helper methods for normalizing log data."""
    @staticmethod
    def normalize(log_data: dict) -> dict:
        """Normalizes a raw log entry into a structured format."""
        # Example normalization: add a timestamp if not present
        if "timestamp" not in log_data:
            import datetime
            log_data["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
        return log_data

    @staticmethod
    def denormalize(normalized_log: dict) -> dict:
        """Denormalizes a structured log entry back to a raw format."""
        return normalized_log
