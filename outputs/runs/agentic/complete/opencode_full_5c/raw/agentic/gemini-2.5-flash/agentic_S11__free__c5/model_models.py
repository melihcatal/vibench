from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ModelRequest:
    prompt: str
    model_id: str
    temperature: Optional[float] = 0.7
    max_output_tokens: Optional[int] = 1024


@dataclass
class ModelResponse:
    text: str
    metadata: Optional[Dict[str, Any]] = None
    safety_attributes: Optional[Dict[str, Any]] = None
    localized_text: Optional[str] = None
    embedding: Optional[List[float]] = None
    audio_content: Optional[bytes] = None
