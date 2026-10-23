from typing import Dict, Any, Optional

class ModelRequest:
    """Defines a generic model request structure."""
    def __init__(self, prompt: str, parameters: Optional[Dict[str, Any]] = None):
        self.prompt = prompt
        self.parameters = parameters if parameters is not None else {}

class ModelResponse:
    """Defines a generic model response structure, with an optional raw response."""
    def __init__(self, text: str, metadata: Optional[Dict[str, Any]] = None, raw_response: Optional[Any] = None):
        self.text = text
        self.metadata = metadata if metadata is not None else {}
        self.raw_response = raw_response

    @classmethod
    def from_vertex_ai_response(cls, va_response: Any, model_name: str = "") -> "ModelResponse":
        text = va_response.text
        metadata = {
            "model_name": model_name,
        }
        if hasattr(va_response, 'usage_metadata'):
            metadata["usage_metadata"] = {
                "prompt_token_count": va_response.usage_metadata.prompt_token_count,
                "candidates_token_count": va_response.usage_metadata.candidates_token_count,
                "total_token_count": va_response.usage_metadata.total_token_count,
            }
        return cls(text=text, metadata=metadata, raw_response=va_response)

