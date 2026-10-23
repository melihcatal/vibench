from typing import TypedDict, List, Dict, Any

class ImageLabels(TypedDict):
    labels: List[Dict[str, Any]]

class ImageDescription(TypedDict):
    description: str

class ImageTexts(TypedDict):
    texts: List[str]

class ImageSafety(TypedDict):
    is_safe: bool
    risks: List[str]
    scores: Dict[str, float]

class VisualAnalysis(TypedDict):
    labels: ImageLabels
    description: ImageDescription
    texts: ImageTexts
    safety: ImageSafety