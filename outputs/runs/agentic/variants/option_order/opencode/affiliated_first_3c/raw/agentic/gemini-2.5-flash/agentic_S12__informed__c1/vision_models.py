import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class ImageDetectionRequest:
    image_uri: str


@dataclasses.dataclass
class LabelDetectionResponse:
    labels: List[str]


@dataclasses.dataclass
class TextDetectionResponse:
    text_annotations: List[str]


@dataclasses.dataclass
class SafeSearchDetectionResponse:
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str
