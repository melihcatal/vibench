# storage_models.py
from pydantic import BaseModel, Field, Extra

class UploadResponse(BaseModel):
    status: str = Field(..., description="Upload result")
    bucket: str = Field(..., description="Bucket name")
    key: str = Field(..., description="Object key")
    class Config:
        arbitrary_types_allowed = True
        allow_mutation = False
        extra = Extra.forbid


class PresignResponse(BaseModel):
    url: str = Field(..., description="Time‑limited download URL")
    class Config:
        allow_mutation = False
        extra = Extra.forbid


class MetadataResponse(BaseModel):
    etag: str = Field(..., description="ETag or checksum")
    content_type: str = Field(..., description="MIME type")
    content_length: int = Field(..., description="Size in bytes")
    last_modified: str = Field(..., description="ISO timestamp")
    class Config:
        allow_mutation = False
        extra = Extra.forbid


class ListResponse(BaseModel):
    Contents: list[dict] = Field(..., description="Object keys under the prefix")
    class Config:
        allow_mutation = False
        extra = Extra.forbid


class OCRResponse(BaseModel):
    text: str = Field(..., description="Extracted plain‑text content")
    class Config:
        allow_mutation = False
        extra = Extra.forbid


class TranslationResponse(BaseModel):
    translated_text: str = Field(..., description="Translated text string")
    class Config:
        allow_mutation = False
        extra = Extra.forbid


class SummaryResponse(BaseModel):
    summary: str = Field(..., description="AI‑generated concise summary")
    class Config:
        allow_mutation = False
        extra = Extra.forbid


class EmbeddingResponse(BaseModel):
    embedding: list[float] = Field(..., description="Vector representation for search")
    class Config:
        allow_mutation = False
        extra = Extra.forbid
