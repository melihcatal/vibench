from model_client import get_generative_model
from model_models import ModelRequest, ModelResponse
from vertexai.generative_models import GenerationResponse


def collect_platform_metadata(request: ModelRequest) -> ModelResponse:
    model = get_generative_model()
    response: GenerationResponse = model.generate_content(
        request.prompt, **request.kwargs
    )

    # Extract metadata from the Vertex AI GenerationResponse object
    metadata = {
        "finish_reason": response.candidates[0].finish_reason.name
        if response.candidates
        else None,
        "token_count": response.usage_metadata.prompt_token_count
        if response.usage_metadata
        else None,
        "candidates_count": len(response.candidates),
    }
    return ModelResponse(
        text=response.text, raw_response=response._raw_response, metadata=metadata
    )
