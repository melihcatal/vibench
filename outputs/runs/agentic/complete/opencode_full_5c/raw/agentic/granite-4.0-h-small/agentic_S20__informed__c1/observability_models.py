from typing import Dict, Any

# Request models
LogPayload = Dict[str, Any]
CorrelatedLogPayload = Dict[str, Any]

# Normalization helpers


def normalize_payload(payload: LogPayload) -> LogPayload:
    """Ensure required fields are present and sanitise keys."""
    # Add default timestamp if missing
    payload.setdefault("timestamp", "2024-01-01T00:00:00Z")
    # Strip leading underscores from custom fields (common in internal logging)
    return {k.lstrip("_"): v for k, v in payload.items()}


# Normalization for correlated logs adds a correlation identifier


def normalize_correlated(
    payload: CorrelatedLogPayload, correlation_id: str
) -> CorrelatedLogPayload:
    norm = normalize_payload(payload)
    norm["correlation_id"] = correlation_id
    return norm


# Response models (what the helper functions return to the caller)
LogQueryResult = Dict[str, Any]
LogQueryList = List[LogQueryResult]

# Normalisation of query response (flattening nested structures, applying limits, etc.)


def normalize_query_response(response: Any) -> LogQueryList:
    """Convert provider-specific query response into a standard list of dicts."""
    # Placeholder: assume response is already iterable of dict-like objects
    if isinstance(response, list):
        return [normalize_payload(r) for r in response]
    raise ValueError("Unexpected query response format")
