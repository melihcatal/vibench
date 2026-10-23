from typing import TypedDict, List, Dict, Any

class LabelsResponse(TypedDict):
    labels: List[str]

class DescriptionResponse(TypedDict):
    description: str

class TextResponse(TypedDict):
    texts: List[str]

class SafetyResponse(TypedDict):
    is_safe: bool
    risks: List[str]
