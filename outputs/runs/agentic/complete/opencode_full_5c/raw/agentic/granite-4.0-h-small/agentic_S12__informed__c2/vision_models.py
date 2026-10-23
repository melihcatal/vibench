# [HELPER] vision_models.py

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class DetectedLabel:
    name: str
    confidence: float


@dataclass
class DetectedText:
    text: str
    bounding_box: List[float]


@dataclass
class ImageDescription:
    text: str
    confidence: float


@dataclass
class SafetyEvaluation:
    unsafe: bool
    issues: List[str]


@dataclass
class ObjectStorageArtifact:
    bucket: str
    key: str
    url: str
