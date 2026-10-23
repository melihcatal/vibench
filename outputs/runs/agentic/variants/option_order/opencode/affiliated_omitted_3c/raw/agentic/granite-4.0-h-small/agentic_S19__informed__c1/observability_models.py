from typing import TypedDict, List, Optional


class DatadogMetricFilter(TypedDict):
    name: str
    values: Optional[List[str]]


class DatadogMetricRequest(TypedDict):
    query: str
    filters: Optional[Dict[str, Any]]


class DatadogMetricResponse(TypedDict):
    series: List[Dict[str, Any]]


# Placeholder for later-step models


class TextSafetyReport(TypedDict):
    safe: bool
    flagged_tokens: Optional[List[str]]


class TranslationResult(TypedDict):
    translated: str


class ExportMetadata(TypedDict):
    object_key: str
    checksum: str
