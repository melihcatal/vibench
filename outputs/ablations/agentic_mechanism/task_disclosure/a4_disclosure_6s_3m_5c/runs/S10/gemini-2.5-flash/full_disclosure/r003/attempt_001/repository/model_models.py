from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

@dataclass
class ModelParameters:
    temperature: float = 0.7
    max_tokens: int = 1024
    top_p: float = 1.0
    top_k: int = 40
    stop_sequences: Optional[List[str]] = None
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

@dataclass
class ModelRequest:
    model_name: str
    prompt: str
    parameters: ModelParameters = field(default_factory=ModelParameters)
    context: Optional[str] = None

@dataclass
class ModelResponse:
    generated_text: str
    model_name: str
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    finish_reason: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

def normalize_response(model_response_data: Dict[str, Any], model_name: str) -> ModelResponse:
    """
    Normalizes a raw model response (e.g., from a hosted LLM API) into a
    standard ModelResponse object. This function would typically handle
    provider-specific response structures.
    """
    # This is a placeholder for actual normalization logic.
    # In a real scenario, you would parse `model_response_data`
    # based on the specific LLM provider's API response format.
    generated_text = model_response_data.get("choices", [{}])[0].get("text", "")
    
    return ModelResponse(
        generated_text=generated_text,
        model_name=model_name,
        raw_response=model_response_data
    )
