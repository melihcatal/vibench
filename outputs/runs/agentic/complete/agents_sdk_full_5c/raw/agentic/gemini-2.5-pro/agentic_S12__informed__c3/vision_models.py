
from dataclasses import dataclass

@dataclass
class Label:
    name: str
    score: float

@dataclass
class ImageDescription:
    description: str
    tags: list[str]

@dataclass
class DetectedText:
    text: str
    confidence: float
    box_id: int

@dataclass
class SafetyScore:
    label: str
    score: float
