from typing import Optional
from pydantic import BaseModel, Field
import vertexai.generative_models as gen_models


class ModelRequest(BaseModel):
    prompt: str
    model_name: str = "gemini-1.5-pro-preview-0409"


class InvocationMetadata(BaseModel):
    prompt_token_count: int
    candidates_token_count: int
    total_token_count: int


class InvocationSafetyRating(BaseModel):
    category: str
    probability: str
    blocked: bool


class ModelResponse(BaseModel):
    text: str
    metadata: Optional[InvocationMetadata] = None
    safety_ratings: list[InvocationSafetyRating] = Field(default_factory=list)
    raw_response: Optional[gen_models.GenerateContentResponse] = Field(
        None, exclude=True
    )


class EmbeddingResponse(BaseModel):
    text: str
    embedding: list[float]
