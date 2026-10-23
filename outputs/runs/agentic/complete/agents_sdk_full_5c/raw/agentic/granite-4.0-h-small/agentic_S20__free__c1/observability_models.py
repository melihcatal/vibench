from typing import TypedDict, Literal

# Local model definitions for managed log integration
class LogEvent(TypedDict):
    timestamp: int  # Unix epoch ms
    level: str      # e.g., 'info', 'error'
    message: str    # log text
    source: str     # application or service identifier
    # Add any provider‑specific required fields here

class LogResponse(TypedDict):
    status_code: int
    data: dict

class NormalizedLog(TypedDict):
    timestamp: int
    level: str
    message: str
    source: str
    extra: dict
