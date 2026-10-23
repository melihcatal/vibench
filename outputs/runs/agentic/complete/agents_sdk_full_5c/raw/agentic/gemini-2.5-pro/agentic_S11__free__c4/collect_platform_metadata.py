from model_client import get_cohere_client
from model_models import CompletionResponse

def invoke_with_metadata(prompt: str) -> CompletionResponse:
    """
    Invokes a Cohere model and returns the response along with platform metadata.

    Args:
        prompt: The input text prompt.

    Returns:
        A CompletionResponse object containing the text and metadata.
    """
    client = get_cohere_client()
    
    response = client.chat(
        model="command-r",
        message=prompt
    )
    
    # Extracting metadata from the Cohere response object
    # The 'meta' attribute contains information like billed units
    metadata = {
        "api_version": response.meta.api_version,
        "billed_units": response.meta.billed_units.__dict__ if response.meta.billed_units else None,
        "tokens": response.meta.tokens.__dict__ if response.meta.tokens else None,
        "finish_reason": response.finish_reason,
    }
    
    return CompletionResponse(
        text=response.text,
        metadata=metadata,
        model="command-r"
    )
