from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ModelInput:
    """Represents a standardized input for model invocation."""
    prompt: str
    parameters: Optional[Dict[str, Any]] = None

@dataclass
class ModelOutput:
    """Represents a standardized output from a model invocation."""
    text: str
    metadata: Optional[Dict[str, Any]] = None
    raw_response: Optional[Any] = None

def normalize_vertex_ai_response(response) -> ModelOutput:
    """Normalizes a Vertex AI generative model response into a ModelOutput."""
    text = ""
    if response.text:
        text = response.text
    
    metadata = {}
    if response.usage_metadata:
        metadata = {
            "prompt_token_count": response.usage_metadata.prompt_token_count,
            "candidates_token_count": response.usage_metadata.candidates_token_count,
            "total_token_count": response.usage_metadata.total_token_count,
        }
    
    return ModelOutput(text=text, metadata=metadata, raw_response=response)
