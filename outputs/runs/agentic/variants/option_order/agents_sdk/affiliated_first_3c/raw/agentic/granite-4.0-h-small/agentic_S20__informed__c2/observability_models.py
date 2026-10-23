from typing import TypedDict

# Normalized request & response shapes used across the same-scenario files

class SimpleLogMsg(TypedDict):
    message: str
    timestamp: str          # ISO 8601, UTC
    level: str              # DEBUG, INFO, WARNING, ERROR
    correlation_id: str | None = None


class LogResultItem(TypedDict):
    timestamp: str
    level: str
    message: str
    correlation_id: str | None
    # Provider may add extra fields; callers should ignore unknown keys
