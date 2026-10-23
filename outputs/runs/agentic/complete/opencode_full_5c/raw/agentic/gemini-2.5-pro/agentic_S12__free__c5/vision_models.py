from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class ImageLabel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    description: str
    score: float


class ImageDescription(BaseModel):
    model_config = ConfigDict(extra="ignore")
    text: str


class ImageText(BaseModel):
    model_config = ConfigDict(extra="ignore")
    text: str
    locale: Optional[str] = None


class ImageSafety(BaseModel):
    model_config = ConfigDict(extra="ignore")
    category: str
    likelihood: str


class VisionAnalysis(BaseModel):
    model_config = ConfigDict(extra="ignore")
    labels: List[ImageLabel]
    description: ImageDescription
    texts: List[ImageText]
    safety: List[ImageSafety]
