from pydantic import BaseModel, Field
from typing import Optional


class SecretRequest(BaseModel):
    secret_name: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


class SecretResponse(BaseModel):
    name: str
    arn: str
    secret_string: str
    created_date: float
    version_id: str


class JsonSecret(BaseModel):
    api_key: str = Field(alias="API_KEY")
    username: str
    password: str


class ContentSafetyRequest(BaseModel):
    text_content: str


class ContentSafetyResponse(BaseModel):
    hate_score: float
    self_harm_score: float
    sexual_score: float
    violence_score: float


class EmbeddingsRequest(BaseModel):
    text_content: str


class EmbeddingsResponse(BaseModel):
    embedding: list[float]


class TranslationRequest(BaseModel):
    text_content: str
    target_language: str
    source_language: Optional[str] = None


class TranslationResponse(BaseModel):
    translated_text: str


class RotationSummaryRequest(BaseModel):
    secret_name: str
    rotation_status: str
    last_rotated: str
    next_rotation: str
