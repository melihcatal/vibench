from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class ModelRequest:
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7
    top_p: float = 1.0
    stop_sequences: Optional[List[str]] = None
    model_id: Optional[str] = None # Specific model identifier if needed

@dataclass
class ModelResponse:
    text: str
    model_id: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = field(default_factory=dict)

def normalize_response(response_data: Dict[str, Any], model_id: str) -> ModelResponse:
    """
    Normalizes a raw LLM provider response into a standard ModelResponse.
    This is a placeholder and would need to be adapted for specific LLM provider responses.
    """
    # Example normalization (this will vary greatly by provider)
    if "choices" in response_data and response_data["choices"]:
        text = response_data["choices"][0].get("text", "")
    elif "generations" in response_data and response_data["generations"]:
        text = response_data["generations"][0].get("text", "")
    else:
        text = str(response_data) # Fallback to string representation of the whole response

    return ModelResponse(text=text, model_id=model_id, raw_response=response_data)
