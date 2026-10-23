from typing import List, Dict, Any, TypedDict


class VisionLabels(TypedDict):
    labels: List[str]


class VisionDescription(TypedDict):
    description: str


class VisionText(TypedDict):
    texts: List[str]


class VisionSafety(TypedDict):
    safe: bool
    violations: List[str]


class FullAnalysis(TypedDict):
    labels: List[str]
    description: str
    texts: List[str]
    safety: Dict[str, Any]
