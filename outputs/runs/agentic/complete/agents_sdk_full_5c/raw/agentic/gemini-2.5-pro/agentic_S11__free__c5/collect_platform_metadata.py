from select_platform_resource import get_model
from model_models import ModelResponseWithMetadata

def invoke_model_with_metadata(prompt: str) -> ModelResponseWithMetadata:
    """
    Invokes a model and returns its output along with platform metadata.

    Args:
        prompt: The input prompt for the model.

    Returns:
        A data class containing the response text and usage metadata.
    """
    model = get_model("gemini-1.5-flash-001")
    
    response = model.generate_content(prompt)
    
    # Extract usage metadata from the provider's response object
    # The structure of this metadata is specific to the Google Vertex AI API
    usage_metadata = {
        "prompt_token_count": response.usage_metadata.prompt_token_count,
        "candidates_token_count": response.usage_metadata.candidates_token_count,
        "total_token_count": response.usage_metadata.total_token_count,
    }

    return ModelResponseWithMetadata(
        text=response.text,
        metadata=usage_metadata
    )
