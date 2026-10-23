from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ModelPayload(BaseModel):
    text: str
    context: Optional[str] = None
    question: Optional[str] = None
    format: Optional[str] = None # e.g., "json"
    target_language: Optional[str] = None # e.g., "fr"

class ModelResponse(BaseModel):
    text: str
    extracted_content: Optional[Dict[str, Any]] = None
    translated_text: Optional[str] = None
    audio_content: Optional[bytes] = None
    embeddings: Optional[List[float]] = None
