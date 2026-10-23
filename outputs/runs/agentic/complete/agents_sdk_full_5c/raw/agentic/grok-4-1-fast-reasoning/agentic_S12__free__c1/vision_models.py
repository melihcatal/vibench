from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ImageLabels:
    labels: List[str]
    confidences: Optional[List[float]] = None

@dataclass
class ImageDescription:
    description: str

@dataclass
class ImageText:
    full_text: str

@dataclass
class ImageSafety:
    adult_score: Optional[float] = None
    racy_score: Optional[float] = None
    gore_score: Optional[float] = None
    ratings: Optional[Dict[str, str]] = None