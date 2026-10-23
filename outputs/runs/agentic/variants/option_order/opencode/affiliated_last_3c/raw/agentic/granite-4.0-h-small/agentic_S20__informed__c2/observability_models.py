from typing import TypedDict, List, Dict


class LogEvent(TypedDict):
    time: int  # epoch seconds
    level: str
    msg: str
    meta: Dict[str, Any]


class LogResponse(TypedDict):
    events: List[LogEvent]
    next_token: Optional[str]


class ErrorEvent(TypedDict):
    timestamp: int
    level: str
    message: str
    exception: str
    stack_trace: str


class ErrorMessage(TypedDict):
    original: str
    translated: str
    language: str


class SafeCheckResult(TypedDict):
    clean: bool
    detected: Optional[List[str]]


class EmbeddingResult(TypedDict):
    vector: List[float]
