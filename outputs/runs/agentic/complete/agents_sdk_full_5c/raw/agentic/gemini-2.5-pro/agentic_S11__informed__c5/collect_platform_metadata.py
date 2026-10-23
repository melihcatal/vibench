from model_client import get_client
from model_models import ResponseWithMetadata
from vertexai.generative_models import GenerativeModel

def invoke_and_collect_metadata(prompt: str) -> ResponseWithMetadata:
    """
    Invokes a Vertex AI model and returns the output along with
    provider-specific metadata.

    Args:
        prompt: The text prompt to send to the model.

    Returns:
        A ResponseWithMetadata object containing the generated text
        and the full provider response object, which includes metadata.
    """
    get_client()

    # Using a specific Google model ID
    model = GenerativeModel("gemini-1.0-pro")
    
    response = model.generate_content(prompt)

    # The `response` object from the vertexai SDK contains metadata
    # such as usage statistics.
    # response.usage_metadata contains token counts.
    
    return ResponseWithMetadata(
        text=response.text,
        provider_response=response
    )
