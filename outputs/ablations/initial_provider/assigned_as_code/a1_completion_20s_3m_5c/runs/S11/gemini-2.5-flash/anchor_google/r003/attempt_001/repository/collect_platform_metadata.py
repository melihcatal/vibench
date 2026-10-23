from google import genai
from model_models import ModelInvocationPayload, ModelConfig, ModelInvocationResponse
from model_client import get_vertex_ai_client
from typing import Dict, Any

def collect_platform_metadata(
    payload: ModelInvocationPayload, config: ModelConfig
) -> ModelInvocationResponse:
    client = get_vertex_ai_client(config.project_id, config.location)
    model = client.get_model(config.model_id)

    response = model.generate_content(
        payload.text
    )

    metadata = {
        "model_id": config.model_id,
        "project_id": config.project_id,
        "location": config.location,
        "prompt_token_count": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
        "candidates_token_count": response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
        # Add other relevant metadata from the response object
        "finish_reason": response.candidates[0].finish_reason.name if response.candidates and response.candidates[0].finish_reason else None,
    }

    return ModelInvocationResponse(
        text=response.text,
        metadata=metadata
    )
