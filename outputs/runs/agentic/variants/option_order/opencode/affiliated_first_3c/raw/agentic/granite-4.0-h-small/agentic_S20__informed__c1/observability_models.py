import json
from typing import TypedDict


class LogEvent(TypedDict):
    timestamp: str
    level: str
    message: str
    request_id: str


class LogResponse(TypedDict):
    status: int
    message: str
    data: dict


class NormalizedLog(TypedDict):
    timestamp: str
    level: str
    message: str
    correlation_id: str


def normalize_log(raw: dict) -> NormalizedLog:
    """Convert a provider-specific log dict into a common schema."""
    return {
        "timestamp": raw.get("timestamp") or raw.get("time"),
        "level": raw.get("severity") or raw.get("level"),
        "message": raw.get("message") or raw.get("msg"),
        "correlation_id": raw.get("request_id"),
    }


def denormalize_response(provider_response) -> LogResponse:
    """Wrap a provider's raw response into a uniform response shape."""
    return {"status": 200, "message": "ok", "data": provider_response}
