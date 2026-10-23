import os
import vertexai
from model_client import get_model_client
from model_models import ModelRequest, ModelResponse
from vertexai.preview.generative_models import GenerationConfig


def collect_model_output_and_metadata(
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

    metadata = {}
    if hasattr(response, "usage_metadata") and response.usage_metadata:
        metadata["prompt_token_count"] = response.usage_metadata.prompt_token_count
        metadata["candidates_token_count"] = (
            response.usage_metadata.candidates_token_count
        )
        metadata["total_token_count"] = response.usage_metadata.total_token_count

    # You might also want to include model name, finish reason, etc.
    if response.candidates and len(response.candidates) > 0:
        candidate = response.candidates[0]
        if hasattr(candidate, "finish_reason"):
            metadata["finish_reason"] = str(candidate.finish_reason)
        # You can add more metadata as needed from the candidate or response objects.

    return ModelResponse(text=response.text, metadata=metadata)
