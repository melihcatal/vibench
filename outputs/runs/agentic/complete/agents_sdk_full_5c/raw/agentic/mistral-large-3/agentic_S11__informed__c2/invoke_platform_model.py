import os
from typing import Optional
from model_client import get_vertex_ai_client
from model_models import ModelRequest, ModelResponse


def invoke_model(
    request: ModelRequest,
    model_id: str = "gemini-1.5-pro-001",
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> ModelResponse:
    """Invoke a Vertex AI managed model with the given request."""
    client = get_vertex_ai_client()
    
    generation_config = {
        "temperature": temperature if temperature is not None else request.temperature,
        "max_output_tokens": max_tokens if max_tokens is not None else request.max_tokens,
    }
    
    model = client.get_generative_model(model_name=model_id, generation_config=generation_config)
    response = model.generate_content(request.prompt)
    
    return ModelResponse(
        output=response.text,
        metadata={
            "model_id": model_id,
            "usage": {
                "prompt_token_count": response.usage_metadata.prompt_token_count,
                "candidates_token_count": response.usage_metadata.candidates_token_count,
                "total_token_count": response.usage_metadata.total_token_count,
            },
        }
    )