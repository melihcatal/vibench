from pydantic import BaseModel, Field
from typing import Optional, Any, List, Dict

class InvocationRequest(BaseModel):
    prompt: str
    model_id: Optional[str] = None # e.g., anthropic.claude-3-haiku-20240307-v1:0
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0

class InvocationResponse(BaseModel):
    generated_text: str
    model_id: Optional[str] = None
    input_token_count: Optional[int] = None
    output_token_count: Optional[int] = None
    raw_metadata: Optional[Dict[str, Any]] = None

class StreamingChunk(BaseModel):
    text_content: str
    raw_event: Optional[Dict[str, Any]] = None
    is_start: Optional[bool] = False
    is_end: Optional[bool] = False
    input_token_count: Optional[int] = None
    output_token_count: Optional[int] = None

class ModelInfo(BaseModel):
    model_id: str
    model_name: str
    provider_name: str
    input_modalities: List[str]
    output_modalities: List[str]
