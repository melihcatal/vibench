# observability_models.py
# Local request/response and normalization helpers for Managed Metrics Monitoring

from __future__ import annotations
from typing import Any, Dict, List, Optional


class QueryRequest:
    """Payload model for querying metric datapoints or statistics."""

    def __init__(
        self,
        metric: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        window: Optional[str] = None,
        dimensions: Optional[Dict[str, str]] = None,
        aggregate: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.metric = metric
        self.start_time = start_time  # ISO 8601 format
        self.end_time = end_time
        self.window = window  # e.g., "P1H" for one hour
        self.dimensions = dimensions  # {label_key: label_value}
        self.aggregate = aggregate  # e.g., "avg", "sum"
        self.extra = kwargs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric": self.metric,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "window": self.window,
            "dimensions": self.dimensions,
            "aggregate": self.aggregate,
            **self.extra,
        }


class QueryResponse:
    """Normalized response model for metric query results."""

    def __init__(self, raw: Dict[str, Any]) -> None:
        self.raw = raw
        self.data = self._normalize(raw)

    def _normalize(self, raw: Dict[str, Any]) -> Any:
        """Convert provider-specific response into a generic shape.
        Returns a list of datapoints [{timestamp: value}, ...] or similar.
        """
        # Example normalization for Datadog (adjust per provider later)
        # Provider could be identified via a context object if needed
        points = raw.get("series", [])
        normalized = []
        for p in points:
            normalized.append(
                {
                    "timestamp": p.get("timestamp"),
                    "value": p.get("value"),
                }
            )
        return normalized

    def get_values(self) -> List[float]:
        return [pt["value"] for pt in self.data if "value" in pt]


class StatsRequest(QueryRequest):
    """Payload model for aggregated statistics (e.g., min, max, avg)."""

    pass


class StatResponse(QueryResponse):
    """Normalized response for aggregated statistics."""

    pass


class DimensionFilterRequest(QueryRequest):
    """Payload model for queries filtered by resource labels or dimensions."""

    pass


class FilterResponse(QueryResponse):
    """Normalized response for filtered metric data."""

    pass


class CompareRequest(QueryRequest):
    """Payload model for comparing two metric series (e.g., resource A vs resource B)."""

    pass


class CompareResponse(QueryResponse):
    """Normalized response for metric comparison series."""

    pass


class MetricSummaryRequest(QueryRequest):
    """Payload model for summarizing recent metric trends or anomalies."""

    pass


class MetricSummaryResponse:
    """Generic response model for summarized metric insights."""

    def __init__(self, raw: Dict[str, Any]) -> None:
        self.raw = raw
        self.summary = self._summarize(raw)

    def _summarize(self, raw: Dict[str, Any]) -> str:
        # Placeholder implementation; replace with provider-specific logic
        return (
            "Recent metric stable"
            if raw.get("stable")
            else "Recent metric anomaly detected"
        )


class SafetyRequest:
    """Payload model for checking free‑text labels/annotations for unsafe content."""

    def __init__(self, text: str, context: Optional[Dict[str, Any]] = None) -> None:
        self.text = text
        self.context = context or {}

    def to_dict(self) -> Dict[str, str]:
        return {"text": self.text, **self.context}


class SafetyResponse:
    """Response indicating whether the supplied text contains unsafe content."""

    def __init__(self, flag: bool, details: Optional[Dict[str, Any]] = None) -> None:
        self.flag = flag
        self.details = details or {}


class LocaleTranslationRequest:
    """Payload model for translating metric or dashboard notes to another locale."""

    def __init__(self, source_text: str, target_locale: str) -> None:
        self.source_text = source_text
        self.target_locale = target_locale

    def to_dict(self) -> Dict[str, str]:
        return {"source": self.source_text, "target_locale": self.target_locale}


class TranslationResponse:
    """Generic response model for translated text."""

    def __init__(self, translated: str) -> None:
        self.translated = translated


class ExportSnapshotRequest(QueryRequest):
    """Payload model for exporting metric snapshots to object storage."""

    pass


class ExportSnapshotResponse:
    """Response containing a URL or reference to the stored snapshot."""

    def __init__(self, storage_ref: str) -> None:
        self.storage_ref = storage_ref
