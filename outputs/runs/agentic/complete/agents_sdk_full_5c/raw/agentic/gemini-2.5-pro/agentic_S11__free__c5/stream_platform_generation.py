from typing import Iterator
from vertexai.generative_models._generative_models import GenerateContentResponse

from select_platform_resource import get_model

def stream_model_generation(prompt: str) -> Iterator[GenerateContentResponse]:
    """
    Streams output from a managed model platform.

    This function yields the provider's raw response objects as they are received.

    Args:
        prompt: The input prompt for the model.

    Yields:
        The provider's response chunks.
    """
    model = get_model("gemini-1.5-flash-001")
    
    # The stream=True parameter enables streaming from the Vertex AI API
    stream = model.generate_content(prompt, stream=True)
    
    for chunk in stream:
        yield chunk
