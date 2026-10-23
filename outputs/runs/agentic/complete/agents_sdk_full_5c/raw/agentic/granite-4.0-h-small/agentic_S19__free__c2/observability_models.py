import re

class ModelValidator:
    """
    Provides local utilities to normalize and validate payloads/ responses for observability APIs.
    These helpers are intentionally generic but are wired to the Google Cloud Monitoring provider.
    """
    @staticmethod
    def normalize_metric_name(name: str) -> str:
        # Ensure metric name conforms to Google's metric type format
        return re.sub(r'^custom/', 'custom.googleapis.com/', name)
    
    @staticmethod
    def normalize_label(labels: dict) -> dict:
        # Keep only whitelisted label keys
        allowed = {'env', 'service', 'version', 'instance_id'}
        return {k: v for k, v in labels.items() if k in allowed}
