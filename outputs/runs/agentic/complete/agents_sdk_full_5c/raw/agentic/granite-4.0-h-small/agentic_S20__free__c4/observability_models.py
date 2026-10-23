from typing import TypedDict, Literal

# Types for structured log payloads

class LogPayload(TypedDict):
    timestamp: str
    message: str
    severity: str

    # Optional correlation identifier
    correlation_id: str | None = None

# Model for a list of logs returned from the API
# Datadog returns hits as a list of objects with the same shape as LogPayload

class LogHit(TypedDict):
    timestamp: str
    message: str
    severity: str
    correlation_id: str | None

# Model for query response

class QueryResponse(TypedDict):
    hits: list[LogHit]
    page: dict
    time: float

# Normalization helper that converts raw API response into our internal LogHit list

def normalize_logs(resp_data: dict) -> list[LogHit]:
    """Convert Datadog's API payload into our TypedDict list."""
    return resp_data.get("logs", [])