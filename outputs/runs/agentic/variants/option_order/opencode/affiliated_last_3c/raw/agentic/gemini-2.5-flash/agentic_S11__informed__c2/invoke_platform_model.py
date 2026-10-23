import os
import vertexai
from model_client import get_model_client
from model_models import ModelRequest, ModelResponse
from vertexai.preview.generative_models import GenerationConfig


def invoke_model(
    request: ModelRequest, project_id: str, location: str
) -> ModelResponse:
    model = get_model_client(project_id, location)

    generation_config_params = {}
    if request.parameters:
        if "temperature" in request.parameters:
            generation_config_params["temperature"] = request.parameters["temperature"]
        if "max_output_tokens" in request.parameters:
            generation_config_params["max_output_tokens"] = request.parameters[
                "max_output_tokens"
            ]
        if "top_p" in request.parameters:
            generation_config_params["top_p"] = request.parameters["top_p"]
        if "top_k" in request.parameters:
            generation_config_params["top_k"] = request.parameters["top_k"]

    generation_config = GenerationConfig(**generation_config_params)

    response = model.generate_content(
        request.prompt, generation_config=generation_config
    )

    # Extract metadata if available. This can vary by model and response structure.
    # For gemini-pro, usage metadata is often within the 'usage_metadata' attribute
    # of the Candidate object or directly in the response if streamed.
    # For simplicity, let's collect basic metadata that might be available.

    metadata = {}
    if hasattr(response, "usage_metadata") and response.usage_metadata:
        metadata["prompt_token_count"] = response.usage_metadata.prompt_token_count
        metadata["candidates_token_count"] = (
            response.usage_metadata.candidates_token_count
        )
        metadata["total_token_count"] = response.usage_metadata.total_token_count

    return ModelResponse(text=response.text, metadata=metadata)
