from typing import TypedDict, List, Dict, Any

class ImageLabels(TypedDict):
    labels: List[str]
    confidence_scores: List[float]

class ImageDescription(TypedDict):
    description: str
    confidence: float

class ImageText(TypedDict):
    texts: List[str]

class ImageSafety(TypedDict):
    categories: Dict[str, float]

class AnalysisArtifacts(TypedDict):
    labels: List[str]
    description: str
    texts: List[str]
    safety: Dict[str, float]
    summary: str
    translated_desc: str
    text_safety: Dict[str, float]