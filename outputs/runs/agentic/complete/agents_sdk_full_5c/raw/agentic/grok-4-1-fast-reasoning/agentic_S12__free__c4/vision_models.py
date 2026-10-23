from typing import List, Optional
from pydantic import BaseModel

class VisionLabels(BaseModel):
    labels: List[str]
    confidence_scores: Optional[List[float]] = None

class ImageDescription(BaseModel):
    description: str

class DetectedText(BaseModel):
    texts: List[str]

class SafetyScores(BaseModel):
    adult: str
    racy: str
    violence: str
    medical: str
    spoof: str

class Summary(BaseModel):
    summary: str

class Translation(BaseModel):
    translated_text: str

class ModerationResult(BaseModel):
    flagged: bool
    categories: Optional[List[str]] = None