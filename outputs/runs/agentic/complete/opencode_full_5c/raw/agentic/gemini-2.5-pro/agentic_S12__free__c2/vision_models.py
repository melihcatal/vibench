from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ImageLabel:
    description: str
    score: float


@dataclass
class ImageText:
    description: str
    bounding_poly: List[Dict[str, int]]


@dataclass
class ImageSafety:
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str


@dataclass
class ImageDescription:
    text: str


@dataclass
class Translation:
    translated_text: str
    detected_language_code: str


@dataclass
class TextSafetyScore:
    attribute: str
    score: float


@dataclass
class ArchiveResult:
    bucket: str
    blob_name: str
    generation: int
