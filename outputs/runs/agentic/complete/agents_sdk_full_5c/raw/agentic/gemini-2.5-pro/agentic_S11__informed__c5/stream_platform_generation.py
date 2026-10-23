from typing import Iterator
from model_client import get_client
from vertexai.generative_models import GenerativeModel, GenerationResponse

def stream_model_generation(prompt: str) -> Iterator[GenerationResponse]:
    """
    Streams the response from a Google Vertex AI model.

    This function preserves the original provider response objects by yielding
    them directly from the SDK.

    Args:
        prompt: The text prompt to send to the model.

    Yields:
        GenerationResponse chunks from the Vertex AI SDK.
    """
    get_client()

    # The model name 'gemini-1.0-pro' is a provider-specific signal
    model = GenerativeModel("gemini-1.0-pro")
    
    # The stream=True parameter enables streaming
    responses = model.generate_content(prompt, stream=True)
    
    for response_chunk in responses:
        yield response_chunk
