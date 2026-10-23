from typing import TypedDict, List, Dict


class ImageLabels(TypedDict):
    labels: List[str]


class ImageDescription(TypedDict):
    description: str


class ImageTexts(TypedDict):
    texts: List[str]


class ImageSafety(TypedDict):
    likelihoods: Dict[str, str]


class VisualAnalysis(TypedDict):
    labels: List[str]
    description: str
    texts: List[str]
    safety: Dict[str, str]
