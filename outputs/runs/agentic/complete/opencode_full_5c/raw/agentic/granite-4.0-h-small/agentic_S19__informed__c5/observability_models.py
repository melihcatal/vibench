# observability_models.py
# LOCAL HELPER – Managed Metrics Monitoring

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class MetricQueryRequest(BaseModel):
    metric: str = Field(
        ..., description="Exact name or identifier of the metric to retrieve."
    )
    start: str = Field(
        ..., description="ISO 8601 formatted start timestamp for the time window."
    )
    end: str = Field(
        ..., description="ISO 8601 formatted end timestamp for the time window."
    )
    dimensions: Optional[Dict[str, str]] = Field(
        None,
        description="Key/value pairs used to filter by resource labels or dimensions.",
    )
    tags: Optional[List[str]] = Field(
        None,
        description="Tag list used by providers that support tag filtering (e.g., Datadog, Azure).",
    )


class MetricQueryResponse(BaseModel):
    metric: str
    datapoints: List[Dict[str, Any]]
    tags: Optional[List[str]] = None
    aggregation: Optional[str] = None


class MetricStatsRequest(BaseModel):
    metric: str
    start: str
    end: str
    aggregate: Optional[str] = None  # e.g., "sum", "avg", "max"
    dimensions: Optional[Dict[str, str]] = None


class MetricStatsResponse(BaseModel):
    metric: str
    statistic: str
    value: float
    dimensions: Optional[Dict[str, str]] = None


class FilteredQueryRequest(BaseModel):
    metric: str
    filter_expr: str = Field(
        ...,
        description='Expression that selects dimensions/labels, e.g., "env=prod and region=us-east".',
    )
    start: str
    end: str


class FilteredQueryResponse(BaseModel):
    metric: str
    datapoints: List[Dict[str, Any]]
    matched_labels: Optional[List[str]] = None


class CompareRequest(BaseModel):
    series_a: FilteredQueryRequest
    series_b: FilteredQueryRequest
    comparison_metric: Optional[str] = None  # e.g., "ratio"


class CompareResponse(BaseModel):
    a: MetricQueryResponse
    b: MetricQueryResponse
    result: Optional[float] = None


class SummaryRequest(BaseModel):
    metric: str
    window: str = Field(..., description='Relative window such as "1h", "24h", "7d".')


class SummaryResponse(BaseModel):
    metric: str
    recent_value: Optional[float] = None
    trend: Optional[str] = None  # \"up\", \"down\", \"stable\"
    anomalies: Optional[List[float]] = None


class AnnotationSafetyCheckRequest(BaseModel):
    free_text: List[str] = Field(
        ..., description="List of strings to inspect for unsafe content."
    )


class AnnotationSafetyCheckResponse(BaseModel):
    safe: bool
    unsafe_items: Optional[List[str]] = None


class TranslateRequest(BaseModel):
    source_locale: str = Field(
        ..., description='BCP‑47 locale of the source text, e.g., "en".'
    )
    target_locale: str = Field(..., description='Locale to translate to, e.g., "fr".')
    texts: List[str] = Field(..., description="Text snippets to translate.")


class TranslateResponse(BaseModel):
    target_locale: str
    translations: List[str]


class ExportSnapshotRequest(BaseModel):
    file_name: str = Field(..., description="Desired name for the exported file.")
    metric: str
    start: str
    end: str
    dimensions: Optional[Dict[str, str]] = None


class ExportSnapshotResponse(BaseModel):
    file_path: str
    storage_url: str
