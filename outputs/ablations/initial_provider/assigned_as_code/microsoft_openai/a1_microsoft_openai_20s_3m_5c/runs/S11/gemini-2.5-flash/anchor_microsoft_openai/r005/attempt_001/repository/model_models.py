import dataclasses
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class ModelRequest:
    prompt: str
    temperature: Optional[float] = 0.7
    max_output_tokens: Optional[int] = 256

@dataclasses.dataclass
class ModelResponse:
    text: str
    metadata: Optional[Dict[str, Any]] = None
    
def normalize_vertex_ai_response(vertex_ai_response: Any) -> ModelResponse:
    """
    Normalizes a Google Cloud Vertex AI model response into a standard ModelResponse.
    """
    text_output = ""
    if vertex_ai_response.candidates:
        for candidate in vertex_ai_response.candidates:
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'text'):
                        text_output += part.text

    metadata = {
        "usage_metadata": {
            "prompt_token_count": vertex_ai_response.usage_metadata.prompt_token_count if hasattr(vertex_ai_response, 'usage_metadata') else None,
            "candidates_token_count": vertex_ai_response.usage_metadata.candidates_token_count if hasattr(vertex_ai_response, 'usage_metadata') else None,
            "total_token_count": vertex_ai_response.usage_metadata.total_token_count if hasattr(vertex_ai_response, 'usage_metadata') else None,
        }
    }

    return ModelResponse(text=text_output, metadata=metadata)
