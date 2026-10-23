from model_client import get_cohere_client
from model_models import ModelRequest, ModelResponse


def collect_platform_metadata(request: ModelRequest) -> ModelResponse:
    """
    Returns model output together with provider platform metadata from Cohere.
    """
    co = get_cohere_client()
    response = co.generate(
        prompt=request.prompt, model="command-r", temperature=request.temperature
    )

    text_generation = response.generations[0].text

    # Cohere API response includes a 'meta' field with rich metadata
    metadata = {
        "id": response.id,
        "api_version": response.meta.get("api_version", {}).get("version"),
        "billed_units": response.meta.get("billed_units"),
        "tokens": response.meta.get("tokens"),
    }

    return ModelResponse(text=text_generation, metadata=metadata)
