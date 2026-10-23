from model_client import get_cohere_client
from model_models import ModelResponse

def collect_platform_metadata(prompt: str) -> ModelResponse:
    """
    Returns model output together with provider platform metadata.

    Args:
        prompt: The input prompt for the model.

    Returns:
        A ModelResponse object containing the generated text and metadata
        from the Cohere API response.
    """
    client = get_cohere_client()
    
    response = client.generate(
        model="command-r",
        prompt=prompt,
        max_tokens=150
    )
    
    generation = response.generations[0]
    text_output = generation.text
    
    # Collect metadata from the provider's response object
    # For Cohere, this includes token counts and other API details.
    metadata = {
        "model": generation.model,
        "finish_reason": str(generation.finish_reason),
        "api_version": response.meta.api_version.version,
        "billed_units": response.meta.billed_units,
    }

    return ModelResponse(
        text=text_output, 
        metadata=metadata,
        provider_response=response
    )
