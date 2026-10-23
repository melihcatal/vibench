from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class BedrockInvokeRequest:
    prompt: str
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    max_tokens: int = 256

@dataclass
class BedrockInvokeResponse:
    text: str
    metadata: Optional[Dict[str, Any]] = None
