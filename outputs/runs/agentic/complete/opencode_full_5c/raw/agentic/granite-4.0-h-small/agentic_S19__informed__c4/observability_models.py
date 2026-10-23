# observability_models.py
# Request, response, and normalization helpers for Managed Metrics Monitoring

from typing import Any, Dict


class MetricRequest:
    """Request model for querying metric data."""

    def __init__(
        self,
        service: str,
        metric: str,
        start_time: str,
        end_time: str,
        window: str = None,
        dimensions: Dict[str, str] = None,
    ):
        self.service = service
        self.metric = metric
        self.start_time = start_time
        self.end_time = end_time
        self.window = window
        self.dimensions = dimensions

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "service": self.service,
            "metric": self.metric,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }
        if self.window:
            data["window"] = self.window
        if self.dimensions:
            data["dimensions"] = self.dimensions
        return data


class MetricResponse:
    """Normalized response structure for metric queries across providers."""

    def __init__(
        self, service: str, metric: str, datapoints: list, metadata: dict = None
    ):
        self.service = service
        self.metric = metric
        self.datapoints = datapoints  # List of (timestamp, value) tuples
        self.metadata = metadata or {}


class GuardrailsResponse:
    """Response model for content safety checks."""

    def __init__(self, safe: bool, issues: list = None):
        self.safe = safe
        self.issues = issues or []


class TranslationRequest:
    """Request model for translating text content."""

    def __init__(self, source_text: str, target_locale: str):
        self.source_text = source_text
        self.target_locale = target_locale


class TranslationResponse:
    """Response model for translation results."""

    def __init__(self, translated_text: str):
        self.translated_text = translated_text
