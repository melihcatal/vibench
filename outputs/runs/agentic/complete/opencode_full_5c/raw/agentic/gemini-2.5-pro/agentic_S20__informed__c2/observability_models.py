from typing import TypedDict, Optional


class StructuredLog(TypedDict):
    message: str
    user_id: str
    request_id: Optional[str]
    severity: str
    context: dict
