from typing import Any, Dict


class SafetyRequest:
    def __init__(self, content: str):
        self.content = content


class SafetyResponse:
    def __init__(self, is_safe: bool, details: Dict[str, Any]):
        self.is_safe = is_safe
        self.details = details
