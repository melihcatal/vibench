from pydantic import BaseModel, Field
from typing import List, Optional


class ImageLabel(BaseModel):
    description: str
    score: float


class ImageDescription(BaseModel):
    text: str


class ImageText(BaseModel):
    text: str
    bounding_poly: List[dict]


class SafetyAnnotation(BaseModel):
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str


class VisionAnalysis(BaseModel):
    labels: Optional[List[ImageLabel]] = None
    description: Optional[ImageDescription] = None
    texts: Optional[List[ImageText]] = None
    safety: Optional[SafetyAnnotation] = None


class ArchiveResult(BaseModel):
    bucket: str
    key: str
    version_id: Optional[str] = Field(None, alias="VersionId")
    etag: Optional[str] = Field(None, alias="ETag")
