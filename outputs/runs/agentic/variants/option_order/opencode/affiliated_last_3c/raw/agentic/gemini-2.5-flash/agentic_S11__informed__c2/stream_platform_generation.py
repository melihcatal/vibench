import os
import vertexai
from model_client import get_model_client
from model_models import ModelRequest, ModelResponse
from vertexai.preview.generative_models import GenerationConfig


def stream_model_generation(request: ModelRequest, project_id: str, location: str):
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

    responses = model.generate_content(
        request.prompt, generation_config=generation_config, stream=True
    )

    for response in responses:
        metadata = {}
        # In streaming, usage_metadata might be in the final response or accumulate.
        # For simplicity, we'll try to capture available text.
        # More sophisticated metadata collection might involve accumulating token counts.

        # Accessing text from streamed response parts
        # The 'text' attribute is on the first candidate's content part.
        response_text = ""
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, "text"):
                            response_text += part.text

        yield ModelResponse(text=response_text, metadata=metadata)
