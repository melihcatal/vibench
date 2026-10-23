from typing import Optional, Dict, Any


class ModelRequest:
    def __init__(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_output_tokens: Optional[int] = None,
    ):
        self.prompt = prompt
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens


class ModelResponse:
    def __init__(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        self.text = text
        self.metadata = metadata if metadata is not None else {}


def normalize_vertex_response(response) -> ModelResponse:
    text = response.text
    metadata = {
        "finish_reason": response.candidates[0].finish_reason.name
        if response.candidates
        else None,
        "token_count": response.usage_metadata.prompt_token_count
        if response.usage_metadata
        else None,
    }
    return ModelResponse(text=text, metadata=metadata)
