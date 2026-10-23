from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ModelInput(BaseModel):
    prompt: str
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)

class ModelOutput(BaseModel):
    text: str
    raw_response: Any  # To hold the raw provider response object
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class EmbeddedOutput(BaseModel):
    embedding: List[float]
    text: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class ModerationResult(BaseModel):
    flagged: bool
    categories: Dict[str, float]
    raw_response: Any

class TranslatedOutput(BaseModel):
    translated_text: str
    source_language: str
    target_language: str
    raw_response: Any

class AudioBriefing(BaseModel):
    audio_content: bytes
    format: str
    raw_response: Any
