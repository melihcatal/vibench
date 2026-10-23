from typing import TypedDict, List, Literal
from datetime import datetime


# ----- LogEvent model used by same‑scenario ingestion files -----
class LogEvent(TypedDict):
    timestamp: int  # epoch milliseconds, supplied by the service if omitted
    message: str
    severity: str  # e.g., "INFO", "ERROR" etc.
    requestId: str  # optional correlation identifier


# ----- Normalized response from a query (common fields) -----
class QueryResult(TypedDict):
    timestamp: datetime
    message: str
    severity: str
    requestId: str | None
    provider: Literal["cloudwatch", "datadog", "gcp", "azure"]


# ----- Normalized response from a text‑safety check -----
class SafetyCheck(TypedDict):
    safe: bool
    flaggedTokens: List[int] | None
    category: str | None


# ----- Normalized payload for translation -----
class TranslatePayload(TypedDict):
    text: str
    target_locale: str


# ----- Normalized embedding request/response -----
class EmbedRequest(TypedDict):
    texts: List[str]


class EmbedResponse(TypedDict):
    embeddings: List[List[float]]
