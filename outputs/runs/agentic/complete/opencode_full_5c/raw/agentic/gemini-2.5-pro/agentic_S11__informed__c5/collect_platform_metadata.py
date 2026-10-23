from vertexai.generative_models import GenerativeModel, Part
from model_models import ModelRequest, ModelResponse


def get_model_response_with_metadata(
    model: GenerativeModel, request: ModelRequest
) -> ModelResponse:
    """
    Returns model output together with provider platform metadata.

    Args:
        model: The GenerativeModel instance to use.
        request: The request object containing the prompt.

    Returns:
        A ModelResponse object containing the generated text and usage metadata.
    """
    part = Part.from_text(request.prompt)
    response = model.generate_content([part])

    usage_metadata = response.usage_metadata
    metadata = {
        "prompt_token_count": usage_metadata.prompt_token_count,
        "candidates_token_count": usage_metadata.candidates_token_count,
        "total_token_count": usage_metadata.total_token_count,
    }

    return ModelResponse(text=response.text, metadata=metadata)
