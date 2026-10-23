from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class InvokeRequest:
    prompt: str
    max_tokens: int = 512
    temperature: float = 0.8
    top_p: float = 0.9

@dataclass
class ModelMetadata:
    input_token_count: Optional[int] = None
    output_token_count: Optional[int] = None
    request_id: Optional[str] = None
    model_id: Optional[str] = None

@dataclass
class InvokeResponse:
    text: str
    metadata: ModelMetadata
